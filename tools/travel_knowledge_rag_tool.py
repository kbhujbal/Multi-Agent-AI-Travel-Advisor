"""
Travel Knowledge RAG Tool - Retrieval-Augmented Generation for travel information
Uses ChromaDB as vector store to retrieve relevant travel tips and information
"""

from langchain.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.schema import Document


class TravelKnowledgeInput(BaseModel):
    """Input schema for Travel Knowledge RAG Tool"""
    query: str = Field(..., description="Question or topic to search for in the travel knowledge base")
    destination: Optional[str] = Field(None, description="Specific destination to filter results")


class TravelKnowledgeRAGTool(BaseTool):
    name: str = "Travel Knowledge Base"
    description: str = (
        "Searches a comprehensive travel knowledge base for tips, guidelines, cultural information, "
        "travel advisories, and best practices. Use this to get expert travel advice, "
        "visa requirements, cultural etiquette, packing tips, and destination-specific information."
    )
    args_schema: Type[BaseModel] = TravelKnowledgeInput

    # Class-level vector store (initialized once)
    _vectorstore: Optional[Chroma] = None
    _initialized: bool = False

    def __init__(self, knowledge_base_path: str = None):
        super().__init__()
        self.knowledge_base_path = knowledge_base_path or "./data/travel_knowledge"

        # Initialize vector store if not already done
        if not TravelKnowledgeRAGTool._initialized:
            self._initialize_vectorstore()
            TravelKnowledgeRAGTool._initialized = True

    def _initialize_vectorstore(self):
        """Initialize ChromaDB vector store with travel documents"""
        print("🔧 Initializing Travel Knowledge RAG system...")

        # Create embeddings
        embeddings = OpenAIEmbeddings()

        # Path to vector store
        persist_directory = "./data/chroma_db"

        # Check if vector store already exists
        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            print("📚 Loading existing vector store...")
            TravelKnowledgeRAGTool._vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
        else:
            print("📚 Creating new vector store from documents...")

            # Ensure knowledge base directory exists
            os.makedirs(self.knowledge_base_path, exist_ok=True)

            # Load documents
            documents = self._load_documents()

            if not documents:
                print("⚠️  No documents found. Creating with sample data...")
                documents = self._create_sample_documents()

            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            splits = text_splitter.split_documents(documents)

            print(f"📄 Loaded {len(documents)} documents, split into {len(splits)} chunks")

            # Create vector store
            TravelKnowledgeRAGTool._vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embeddings,
                persist_directory=persist_directory
            )

            print("✅ Vector store created and persisted")

    def _load_documents(self) -> List[Document]:
        """Load all text documents from knowledge base directory"""
        documents = []

        # Try loading .txt files
        if os.path.exists(self.knowledge_base_path):
            try:
                loader = DirectoryLoader(
                    self.knowledge_base_path,
                    glob="**/*.txt",
                    loader_cls=TextLoader
                )
                documents = loader.load()
            except Exception as e:
                print(f"⚠️  Error loading documents: {e}")

        return documents

    def _create_sample_documents(self) -> List[Document]:
        """Create sample travel documents if none exist"""
        sample_docs = [
            Document(
                page_content="""
                TRAVEL TIPS FOR EUROPE

                Visa Requirements:
                - US citizens can travel to most EU countries for up to 90 days without a visa
                - Starting 2024, ETIAS authorization will be required
                - Always check specific country requirements before travel

                Currency:
                - Euro (€) is used in 20 EU countries
                - Credit cards widely accepted, but carry some cash
                - Notify your bank before traveling

                Transportation:
                - Trains are efficient and connect major cities
                - Consider a Eurail pass for multiple countries
                - Budget airlines offer cheap inter-city flights
                - Metro systems in major cities are excellent

                Cultural Etiquette:
                - Tipping: 5-10% in restaurants (varies by country)
                - Dress modestly when visiting religious sites
                - Learn basic phrases in local language
                - Siesta time in Southern Europe (2-5 PM)
                """,
                metadata={"destination": "Europe", "category": "General Tips"}
            ),
            Document(
                page_content="""
                ITALY TRAVEL GUIDE

                Best Time to Visit:
                - April to June: Pleasant weather, fewer crowds
                - September to October: Beautiful fall colors
                - Avoid August: Peak tourist season, many locals on vacation

                Must-See Cities:
                - Rome: Ancient history, Vatican, Colosseum (3-4 days)
                - Florence: Renaissance art, Uffizi Gallery (2-3 days)
                - Venice: Canals, St. Mark's Basilica (2 days)
                - Milan: Fashion, Da Vinci's Last Supper (1-2 days)

                Food Culture:
                - Coffee: Cappuccino only before 11 AM
                - Meal times: Lunch 12:30-2:30 PM, Dinner after 8 PM
                - Coperto: Cover charge at restaurants (€2-5)
                - Aperitivo: Pre-dinner drinks with snacks (6-9 PM)

                Transportation:
                - High-speed trains (Trenitalia, Italo) between cities
                - Book train tickets in advance for best prices
                - ZTL zones in city centers: No cars without permits
                """,
                metadata={"destination": "Italy", "category": "Country Guide"}
            ),
            Document(
                page_content="""
                PARIS TRAVEL ESSENTIALS

                Top Attractions:
                - Eiffel Tower: Book tickets online in advance
                - Louvre Museum: Wednesday/Friday open late, skip-the-line essential
                - Notre-Dame: Currently under reconstruction
                - Versailles: Full day trip, buy combo tickets
                - Montmartre: Free, charming neighborhood

                Food & Dining:
                - Boulangeries: Fresh bread and pastries daily
                - Cafés: Pay more to sit, cheaper at the bar
                - Markets: Marché Bastille (Thursday/Sunday)
                - Michelin dining: Book 2-3 months ahead

                Transportation:
                - Metro: Efficient, buy carnet (10 tickets) for savings
                - Museum Pass: Skip lines at 60+ attractions
                - Vélib: Bike sharing system
                - Walking: Many areas best explored on foot

                Tips:
                - Learn basic French phrases (locals appreciate effort)
                - Pharmacy = Pharmacie (green cross sign)
                - Sundays: Many shops closed
                """,
                metadata={"destination": "Paris", "category": "City Guide"}
            ),
            Document(
                page_content="""
                PACKING TIPS FOR INTERNATIONAL TRAVEL

                Essential Documents:
                - Passport (valid 6+ months beyond travel)
                - Visa/ETIAS if required
                - Travel insurance documents
                - Copies of important documents (digital + physical)
                - Credit cards + small amount of local currency

                Clothing:
                - Pack versatile, mix-and-match items
                - Comfortable walking shoes (broken in)
                - Layers for varying temperatures
                - One dressy outfit for nice restaurants
                - Check weather forecast before packing

                Electronics:
                - Universal power adapter
                - Portable charger
                - Phone/camera + chargers
                - Download offline maps

                Toiletries:
                - Travel-size essentials (3.4oz for carry-on)
                - Medications in original containers
                - Hand sanitizer and wipes
                - Sunscreen

                Pro Tips:
                - Roll clothes to save space
                - Use packing cubes for organization
                - Wear bulkiest items on plane
                - Leave room for souvenirs
                """,
                metadata={"category": "Packing"}
            ),
            Document(
                page_content="""
                LUXURY TRAVEL TIPS

                Accommodations:
                - 5-star hotels and boutique properties
                - Consider hotel loyalty programs
                - Book suites for special occasions
                - Private villas for groups/families

                Dining:
                - Michelin-starred restaurants (book months ahead)
                - Private chef experiences
                - Wine pairing dinners
                - Exclusive food tours

                Transportation:
                - Business/First class flights
                - Private airport transfers
                - Chauffeur services
                - Luxury train journeys (Orient Express, etc.)

                Experiences:
                - Private museum tours after hours
                - Exclusive wine tastings at châteaux
                - Helicopter tours
                - Private yacht charters
                - Spa and wellness retreats

                Services:
                - Concierge services
                - Personal shopping
                - Private guides
                - Travel planners
                """,
                metadata={"category": "Luxury Travel"}
            ),
            Document(
                page_content="""
                HONEYMOON PLANNING GUIDE

                Best Honeymoon Destinations:
                - Italy: Romance, food, history
                - Maldives: Beach paradise, overwater bungalows
                - Paris: City of love
                - Santorini: Stunning sunsets
                - Bali: Culture, beaches, luxury resorts

                Planning Timeline:
                - 6-9 months before: Book flights and accommodations
                - 3-4 months: Plan activities and experiences
                - 1 month: Confirm all reservations
                - 1 week: Arrange special surprises

                Special Touches:
                - Room upgrades and decorations
                - Couples' spa treatments
                - Private romantic dinners
                - Sunset cruises
                - Champagne and amenities

                Budget Tips:
                - Travel shoulder season for better prices
                - Mention honeymoon when booking (free upgrades!)
                - Bundle packages can save money
                - Mix luxury with budget-friendly activities

                Practical Advice:
                - Register for honeymoon fund instead of gifts
                - Get travel insurance
                - Have backup plans for weather
                - Don't over-schedule - relax and enjoy
                """,
                metadata={"category": "Honeymoon"}
            )
        ]

        # Save sample documents
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        for i, doc in enumerate(sample_docs):
            file_path = os.path.join(
                self.knowledge_base_path,
                f"{doc.metadata.get('destination', doc.metadata.get('category', f'doc_{i}'))}.txt"
            )
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.page_content)

        return sample_docs

    def _run(self, query: str, destination: Optional[str] = None) -> str:
        """
        Search the travel knowledge base

        Args:
            query: The search query
            destination: Optional destination filter
        """
        if not TravelKnowledgeRAGTool._vectorstore:
            return "❌ Knowledge base not initialized. Please check configuration."

        try:
            # Build search query
            search_query = query
            if destination:
                search_query = f"{destination} {query}"

            # Perform similarity search
            results = TravelKnowledgeRAGTool._vectorstore.similarity_search(
                search_query,
                k=3  # Return top 3 most relevant chunks
            )

            if not results:
                return f"No relevant information found for: {query}"

            # Format results
            response = f"## Travel Knowledge Base Results\n\n"
            response += f"**Query:** {query}\n\n"

            for idx, doc in enumerate(results, 1):
                response += f"### Result {idx}\n"
                response += f"{doc.page_content.strip()}\n\n"
                if doc.metadata:
                    response += f"*Source: {doc.metadata}*\n\n"
                response += "---\n\n"

            return response

        except Exception as e:
            return f"❌ Error searching knowledge base: {str(e)}"
