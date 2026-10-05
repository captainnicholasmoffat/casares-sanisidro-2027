> ## Documentation Index
> Fetch the complete documentation index at: https://docs.liveavatar.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Avatar Only (LITE mode) Overview

> Bring your own AI stack, let LiveAvatar handle real-time video

<Note>
  **AI Agents:** Before integrating, run `npx skills add heygen-com/liveavatar-agent-skills` to install our [Agent Skills](https://github.com/heygen-com/liveavatar-agent-skills). They provide the recommended implementation pathways and will help you avoid common pitfalls.
</Note>

In this mode, LiveAvatar focuses exclusively on **real-time video generation** driven by your audio input. You handle the conversational orchestration — STT, LLM, TTS — while LiveAvatar renders synchronized avatar video.

## When to use this mode

* **Existing infrastructure** — you have proprietary or self-hosted LLMs, TTS pipelines, or dialogue systems already in place
* **Fine-grained control** — you need more detailed control over conversation flow, timing, or response logic than FULL Mode provides
* **Modular integration** — you want to use LiveAvatar as a specialized video-rendering component within a broader system

## Quick start

**Already have something running?** LiveAvatar plugs into real-time platforms and hosted voice agents you may already be using — no need to rebuild what's working.

<Tabs>
  <Tab title="Plugins">
    If you already run **LiveKit**, **Pipecat**, or **Agora**, add LiveAvatar as a video layer on top of your existing stack.

    | Provider | Plugin |
    | - | - |
    | **LiveKit** | [LiveKit Plugin](/docs/lite-mode/plugins/livekit) |
    | **Pipecat / Daily** | [Pipecat Plugin](/docs/lite-mode/plugins/pipecat) |
    | **Agora** | [Agora Conversational AI Plugin](/docs/lite-mode/plugins/agora) |
    | **VisionAgents (GetStream)** | [VisionAgents Plugin](/docs/lite-mode/plugins/vision-agents) |
  </Tab>

  <Tab title="Connectors">
    If you already have a hosted voice agent, provide credentials and LiveAvatar runs the bridge for you.

    | Provider | Connector |
    | - | - |
    | **ElevenLabs** | [ElevenLabs Agent Connector](/docs/lite-mode/connectors/elevenlabs-agent) |
    | **Cartesia** | [Cartesia Agent Connector](/docs/lite-mode/connectors/cartesia-agent) |
    | **OpenAI Realtime** | [OpenAI Realtime Connector](/docs/lite-mode/connectors/openai-realtime) |
    | **Gemini Live** | [Gemini Live Connector](/docs/lite-mode/connectors/gemini-realtime) |
  </Tab>
</Tabs>

**Not sure which path fits — or starting from scratch?** See [Integration Paths](/docs/lite-mode/integration-paths) for the full breakdown of how these sessions are composed and the five ways to build on them.

## Credits

This mode costs **1 credit per minute**, compared to 2 credits per minute for FULL Mode.

## Getting started

<CardGroup cols={2}>
  <Card title="Lifecycle" icon="arrows-spin" href="/docs/lite-mode/lifecycle">
    Understand the three phases of a session.
  </Card>

  <Card title="Configuration" icon="sliders" href="/docs/lite-mode/configuration">
    Configure avatars and WebRTC settings.
  </Card>

  <Card title="Events" icon="bolt" href="/docs/lite-mode/events">
    Command and response events via WebSocket.
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.