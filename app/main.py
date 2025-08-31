from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from app.intercom import IntercomClient
from app.ai import AIService
from app.config import settings
from app.utils import validate_webhook_signature
from app.database.knowledge_base import knowledge_base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Intercom AI Support",
    description="AI-powered customer support integration with Intercom",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
intercom_client = IntercomClient()
ai_service = AIService()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class WebhookPayload(BaseModel):
    type: str
    data: dict
    created_at: int
    delivery_status: Optional[str] = None


class ConversationRequest(BaseModel):
    conversation_id: str
    message: str


class DocumentRequest(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}
    document_id: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    k: int = 5


@app.get("/")
async def root():
    """Serve the main application interface"""
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Intercom AI Support"}


@app.post("/webhook/intercom")
async def intercom_webhook(payload: WebhookPayload):
    """Handle Intercom webhook events"""
    try:
        # Validate webhook signature (if configured)
        if settings.INTERCOM_WEBHOOK_SECRET:
            # Note: In production, you'd validate the signature here
            pass

        logger.info(f"Received webhook: {payload.type}")

        if payload.type == "conversation.user.created":
            await handle_new_conversation(payload.data)
        elif payload.type == "conversation.user.replied":
            await handle_user_reply(payload.data)

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Webhook processing failed")


@app.post("/conversation/respond")
async def respond_to_conversation(request: ConversationRequest):
    """Manually trigger AI response to a conversation"""
    try:
        response = await ai_service.generate_response(request.message)

        # Send response to Intercom
        await intercom_client.reply_to_conversation(
            conversation_id=request.conversation_id,
            message=response
        )

        return {"status": "success", "response": response}

    except Exception as e:
        logger.error(f"Conversation response error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to respond to conversation")

# Knowledge Base Management Endpoints


@app.get("/knowledge-base/stats")
async def get_knowledge_base_stats():
    """Get knowledge base statistics"""
    try:
        stats = knowledge_base.get_knowledge_base_stats()
        return {"status": "success", "stats": stats}
    except Exception as e:
        logger.error(f"Error getting knowledge base stats: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to get knowledge base stats")


@app.post("/knowledge-base/search")
async def search_knowledge_base(request: SearchRequest):
    """Search the knowledge base"""
    try:
        documents = knowledge_base.search_knowledge_base(
            request.query, request.k)
        return {"status": "success", "documents": documents}
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to search knowledge base")


@app.post("/knowledge-base/add")
async def add_document(request: DocumentRequest):
    """Add a document to the knowledge base"""
    try:
        success = knowledge_base.add_document(
            content=request.content,
            metadata=request.metadata,
            document_id=request.document_id
        )
        if success:
            return {"status": "success", "message": "Document added successfully"}
        else:
            raise HTTPException(
                status_code=500, detail="Failed to add document")
    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add document")


@app.put("/knowledge-base/update/{document_id}")
async def update_document(document_id: str, request: DocumentRequest):
    """Update a document in the knowledge base"""
    try:
        success = knowledge_base.update_document(
            document_id=document_id,
            content=request.content,
            metadata=request.metadata
        )
        if success:
            return {"status": "success", "message": "Document updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logger.error(f"Error updating document: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to update document")


@app.delete("/knowledge-base/delete/{document_id}")
async def delete_document(document_id: str):
    """Delete a document from the knowledge base"""
    try:
        success = knowledge_base.delete_document(document_id)
        if success:
            return {"status": "success", "message": "Document deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to delete document")


@app.get("/knowledge-base/document/{document_id}")
async def get_document(document_id: str):
    """Get a specific document from the knowledge base"""
    try:
        document = knowledge_base.get_document(document_id)
        if document:
            return {"status": "success", "document": document}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logger.error(f"Error getting document: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get document")


async def handle_new_conversation(data: dict):
    """Handle new conversation creation"""
    conversation_id = data.get("id")
    message = data.get("conversation_message", {}).get("body", "")

    if message:
        response = await ai_service.generate_response(message)
        await intercom_client.reply_to_conversation(conversation_id, response)


async def handle_user_reply(data: dict):
    """Handle user replies to conversations"""
    conversation_id = data.get("conversation", {}).get("id")
    message = data.get("conversation_message", {}).get("body", "")

    if message and conversation_id:
        response = await ai_service.generate_response(message)
        await intercom_client.reply_to_conversation(conversation_id, response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
