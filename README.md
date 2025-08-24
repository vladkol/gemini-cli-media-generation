# Gemini CLI Video Assistant

A demonstration of using [MCP Servers for Genmedia](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/main/experiments/mcp-genmedia/sample-agents/geminicli)
in [Gemini CLI](https://github.com/google-gemini/gemini-cli)
with planned iterative ideation and media generation.

Files in `prompts`, `generated_images` and `generated_videos` directories
are examples of using the setup for creating a video with the following initial idea:

    I want to create a viral funny video with a squirrel on a beach inviting all AI developers
    to "Accelerate AI with Cloud Run" workshops.

It uses Imagen 4 and Veo 3 models through **MCP Servers for Genmedia**.

## How to try

1. Clone this repository:

    ```bash
    git clone https://github.com/vladkol/gemini-cli-media-generation
    ```

2. Clone [vertex-ai-creative-studio repository](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio) inside this repo's clone:

    ```bash
    cd gemini-cli-media-generation
    git clone https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio
    ```

3. Create a Cloud Storage Bucket, let `Vertex AI Service Agent` service account read and write access to the bucket. Vertex AI Service Agent is `service-PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com` account PROJECT_NUMBER is your project's number).

4. Create `.env` file with your Google Cloud Project Id, location/region, and the bucket name.
Use `.env.template` as a starter.

5. Install [MCP Servers for Genmedia](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/mcp-genmedia-go/README.md#getting-started-installation).

6. Configure [MCP Servers in Gemini CLI](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/main/experiments/mcp-genmedia/sample-agents/geminicli). Use [.gemini/settings.sample.json](.gemini/settings.sample.json) as a starter (we only need Imagen, Veo and AVTool servers).

7. Run [Gemini CLI](https://github.com/google-gemini/gemini-cli)!

8. Create your videos!

## NOTE

This project is a demonstration of vibe coding intended to provide a trustworthy and verifiable example that developers and researchers can use. It is not intended for use in a production environment.
