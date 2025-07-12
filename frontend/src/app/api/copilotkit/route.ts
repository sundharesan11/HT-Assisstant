import {
    CopilotRuntime,
    OpenAIAdapter,
    ExperimentalEmptyAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
  } from "@copilotkit/runtime";
  
  import { AgnoAgent } from "@ag-ui/agno"
  // import { AgnoTeam } from "@ag-ui/agno"

  import { NextRequest } from "next/server";
  import { OpenAI } from "openai";
  
  // 1. For multi-agent support, you can still use the empty adapter
  //    or choose a different service adapter based on your needs
  
  // const serviceAdapter = new ExperimentalEmptyAdapter();
  const openai = new OpenAI({
    apiKey: process.env["OPENAI_API_KEY"] ,
  });
   
  const serviceAdapter = new OpenAIAdapter({ openai });
  
  // 2. Create the CopilotRuntime instance with four agents
  const runtime = new CopilotRuntime({
    agents: {
      // Agent 0:
      "agno_agent": new AgnoAgent({
        url: "http://localhost:8000/agui"
      }),
    }
  });
  
  // 3. Build a Next.js API route that handles the CopilotKit runtime requests
  export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: "/api/copilotkit",
    });
  
    return handleRequest(req);
  };
   