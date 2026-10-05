> ## Documentation Index
> Fetch the complete documentation index at: https://docs.liveavatar.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Firewall Configuration

> Network requirements for LiveAvatar WebRTC connections

LiveAvatar uses LiveKit for WebRTC. Connections require WebSocket (WSS) and WebRTC (TLS/DTLS) protocols over TCP and UDP with encrypted connections.

## Minimum required

| Host | Port | Purpose |
| - | - | - |
| `*.livekit.cloud` | TCP 443 | Secure WebSocket signaling |
| `*.turn.livekit.cloud` | TCP 443 | TURN over TLS fallback |
| `*.host.livekit.cloud` | UDP 3478 | TURN/UDP for peer-to-peer |
| `api.liveavatar.com` | TCP 443 | Avatar API and signaling |

## Recommended for best performance

* **All hosts**: UDP 50000–60000 for WebRTC media
* **All hosts**: TCP 7881 for WebRTC TCP fallback

## Tips

* Enable UDP hole-punching where supported
* Avoid symmetric NAT configurations when possible
* UDP is strongly recommended for low-latency performance; TCP fallback degrades quality

## Wildcard alternatives

If your firewall doesn't support wildcards like `*.livekit.cloud`, consult [LiveKit's firewall documentation](https://docs.livekit.io/home/cloud/firewall/) using subdomain `heygen-feapbkvq`.

## Troubleshooting

### Verify browser compatibility

Run the [WebRTC browser test](https://livekit.io/webrtc/browser-test) on the client's machine. It checks that the browser supports the APIs LiveAvatar needs and that nothing is blocking them.

Confirm the following are not blocked:

* **Camera and microphone permissions** — a session requires the browser to grant media device access. Blocked or denied permissions prevent media from flowing.
* **WebRTC** — some privacy extensions, enterprise policies, or browser flags disable WebRTC entirely.
* **Insecure context** — getUserMedia and WebRTC require HTTPS (or `localhost`). Pages served over plain HTTP cannot start a session.

### Verify end-to-end connection

If the firewall and browser checks pass but sessions still fail, walk the full connection path manually. Each step isolates where the failure occurs.

<Steps>
  <Step title="Create a session token">
    Use your API key to request a session token. See [Create Session Token](https://docs.liveavatar.com/api-reference/sessions/create-session-token).

    ```bash theme={null}
    curl -X POST https://api.liveavatar.com/v1/sessions/token \
      -H "X-API-KEY: <YOUR_API_KEY>" \
      -H "accept: application/json" \
      -H "content-type: application/json" \
      -d '{
        "mode": "FULL",
        "avatar_id": "<avatar_id>",
        "avatar_persona": {
          "voice_id": "<voice_id>",
          "context_id": "<context_id>",
          "language": "en"
        }
      }'
    ```

    The response returns a `session_id` and `session_token`. A failure here points to an API key or request issue, not a network one.
  </Step>

  <Step title="Start a session">
    Use the session token to start the session. See [Start Session](https://docs.liveavatar.com/api-reference/sessions/start-session).

    ```bash theme={null}
    curl -X POST https://api.liveavatar.com/v1/sessions/start \
      -H "accept: application/json" \
      -H "authorization: Bearer <session_token>"
    ```

    On success, the response returns `livekit_url` and `livekit_client_token` for the created WebRTC room.
  </Step>

  <Step title="Test the WebRTC room connection">
    Pass the `livekit_url` and `livekit_client_token` from the previous step to the [connection tester](https://livekit.io/connection-test) to confirm the client can reach the WebRTC room.

    If the connection fails or the test shows degraded results, the firewall is likely blocking the required hosts, ports, or UDP media. Re-check the [Minimum required](#minimum-required) hosts and ports above.
  </Step>
</Steps>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.