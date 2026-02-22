import asyncio
import os

from dotenv import load_dotenv
from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.utils.workflow import draw_all_possible_flows

# Set your API key (or use Gemini, Anthropic, etc. via their respective LlamaIndex integrations)
load_dotenv()

MODEL="gemini-3.1-pro-preview" # @param ["gemini-3.1-pro-preview", "gemini-3-pro-preview", "gemini-2.5-pro", "gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.5-flash-lite", ]
PROJECT_ID=os.getenv("GCP_PROJECT_ID")
LOCATION=os.getenv("GCP_LOCATION")

# ==========================================
# 1. Define Custom Events
# These act as the "messengers" passing state between our steps.
# ==========================================

class RetrieveContextEvent(Event):
    """Triggered to start gathering architecture and threat intelligence."""
    system_description: str

class ConductStrideAnalysisEvent(Event):
    """Triggered once all data is collected, signaling the LLM to begin analysis."""
    system_description: str
    architecture_docs: str
    threat_intel_docs: str

# ==========================================
# 2. Define the Agentic Workflow
# ==========================================

class StrideThreatModeler(Workflow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the LLM that will act as the reasoning engine
        self.llm = GoogleGenAI(
            model=MODEL,
            vertexai_config={"project": PROJECT_ID, "location": LOCATION}
        )

    @step
    async def analyze_request(self, ev: StartEvent) -> RetrieveContextEvent:
        """Step 1: Receive the user's system description and trigger retrieval."""
        print(f"🚀 Initialization: Starting threat model for: {ev.system_description}")
        
        # Emitting this event triggers the next step
        return RetrieveContextEvent(system_description=ev.system_description)

    @step
    async def retrieve_sources(self, ev: RetrieveContextEvent) -> ConductStrideAnalysisEvent:
        """Step 2: Retrieve context from multiple RAG sources."""
        print("🔍 Retrieval Agent: Fetching architectural diagrams and internal documentation...")
        
        # MOCK RAG RETRIEVAL 1: System Architecture
        # In a real app, you would query an index here: await index.as_query_engine().aquery(...)
        mock_arch_docs = (
            f"System Architecture for '{ev.system_description}': "
            "Traffic routes through AWS API Gateway to AWS Lambda. "
            "User uploads are stored in a public-facing, unencrypted S3 bucket. "
            "No rate-limiting is currently configured."
        )
        
        print("🔍 Retrieval Agent: Fetching latest STRIDE threat intelligence and CVEs...")
        
        # MOCK RAG RETRIEVAL 2: Threat Intel Database
        mock_threat_intel = (
            "Threat Intel Guidelines: \n"
            "- S3 buckets without encryption/IAM restrictions are highly susceptible to Information Disclosure.\n"
            "- API Gateways without rate limiting are vulnerable to Denial of Service (DoS) attacks."
        )

        # Fire the next event, packing all the gathered context together
        return ConductStrideAnalysisEvent(
            system_description=ev.system_description,
            architecture_docs=mock_arch_docs,
            threat_intel_docs=mock_threat_intel
        )

    @step
    async def generate_stride_report(self, ev: ConductStrideAnalysisEvent) -> StopEvent:
        """Step 3: The LLM synthesizes the data to generate the final STRIDE model."""
        print("🧠 Analysis Agent: Conducting STRIDE analysis...\n")
        
        prompt = f"""
        You are an expert cybersecurity architect. Perform a STRIDE threat model analysis based on the following context.
        
        System Description: {ev.system_description}
        
        Retrieved Architecture Context: 
        {ev.architecture_docs}
        
        Retrieved Threat Intelligence: 
        {ev.threat_intel_docs}
        
        Instructions:
        Output a structured STRIDE analysis identifying specific threats and actionable mitigations for:
        1. Spoofing
        2. Tampering
        3. Repudiation
        4. Information Disclosure
        5. Denial of Service
        6. Elevation of Privilege
        """
        
        response = await self.llm.acomplete(prompt)
        
        # StopEvent halts the workflow and returns the final payload back to the user
        return StopEvent(result=str(response))

# ==========================================
# 3. Execute the Workflow
# ==========================================
async def main():
    # Instantiate the workflow (timeout in seconds)
    workflow = StrideThreatModeler(timeout=120, verbose=False)

    # draw_all_possible_flows(workflow, filename="stride_workflow.html")
    
    # Run the workflow by passing data into the implicit StartEvent
    result = await workflow.run(
        system_description="A new photo-sharing mobile app back-end."
    )
    
    print("="*60)
    print("🛡️ FINAL THREAT MODEL REPORT 🛡️")
    print("="*60)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())