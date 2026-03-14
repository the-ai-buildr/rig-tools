#!/bin/bash

# Well Dashboard Startup Script
# Starts both FastAPI backend and Streamlit frontend

echo "🛢️  Well Dashboard - Starting up..."
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p db exports templates

# Build and start the application
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Well Dashboard is running!"
    echo ""
    echo "🌐 Access the applications:"
    echo "   Frontend (Streamlit): http://localhost:8501"
    echo "   Backend API (FastAPI): http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📋 Default Login Credentials:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "📖 For more information, see README.md"
    echo ""
    echo "Useful commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop: docker-compose down"
    echo "   Restart: docker-compose restart"
else
    echo "❌ Failed to start containers. Check logs with: docker-compose logs"
    exit 1
fi
