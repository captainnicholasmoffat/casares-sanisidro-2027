> ## Documentation Index
> Fetch the complete documentation index at: https://docs.liveavatar.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuration

> Configure avatars and WebRTC settings for Avatar Only mode

This mode offers customization for two main areas: **avatars** and **WebRTC configuration**.

## Avatars

Each avatar is identified by a unique `avatar_id`. LiveAvatar offers a catalog of avatars ranging from realistic human presenters to stylized or expressive characters.

Browse available avatars through the [List Public Avatars](/api-reference/avatar/list-public-avatars) or [List User Avatars](/api-reference/avatar/list-user-avatars) endpoints.

## WebRTC Configuration

### LiveKit (default)

By default, LiveAvatar creates a LiveKit room and provides an agent token. You configure your own ASR, LLM, and TTS stack with a custom LiveKit Agent.

### Bring your own infrastructure

You can provide your own WebRTC setup using:

* **Agora** — configured via the `agora_config` parameter
* **LiveKit** — configured via the `livekit_config` parameter

When using custom infrastructure, LiveAvatar streams the avatar video directly into your WebRTC setup.

## Example

```json theme={null}
{
  "mode": "LITE",
  "avatar_id": "<avatar_id>",
  "video_settings": {
    "quality": "high",
    "encoding": "H264"
  }
}
```

<Warning>
  `encoding: "VP8"` is deprecated and will be removed in a future release. Use `H264` (the default).
</Warning>

With custom LiveKit infrastructure:

```json theme={null}
{
  "mode": "LITE",
  "avatar_id": "<avatar_id>",
  "livekit_config": {
    "url": "wss://your-livekit-server.com",
    "token": "<your_agent_token>"
  }
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.