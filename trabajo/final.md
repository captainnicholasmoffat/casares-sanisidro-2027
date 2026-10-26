**Profesor digital: precios 2026 (leídos el 05-10-2026)**
[V] verificado en página del proveedor · [P] secundaria · [C] cálculo propio. El número remite a la fuente (con fecha, al final).

**1. Avatar en tiempo real**
- LiveAvatar (HeyGen), modo LITE: "Avatar Only (LITE mode) | 1 credit per minute"; "Business | $475 | 6,000 +10 | $0.09/credit" [1][V] → US$0,079/min [C: 475÷6.000]. Español: no figura explícito; el video sale "driven by your audio input" (el idioma lo pone tu TTS) [1]. "rates down to $0.01/min" solo Enterprise negociado [2][V].
- Anam: "$0.11 per extra minute" (Professional); "from $0.04 per minute at scale" (Enterprise); "70+" idiomas [3][V].
- Tavus: "$0.26 per minute" (mejor plan publicado; incluye STT/LLM/TTS) [4][V].
- D-ID: "0.5 credits" cada 15 s hablados [5][V]; precio del crédito no visible → no calculable.
- Simli, Akool: precio por minuto/crédito no encontrado.
- Alibaba 虚拟数字人 (3D, consola china): "0.60 元/路/分钟" [6][V] → US$0,089/min [C: ÷6,7046 CNY/USD, BCE [22]].
- Tencent 数智人 2D interactivo: "27,000元/年/路" (por canal simultáneo, no por minuto) [7][V].
- Baidu 曦灵 2D interactivo: "专属并发1年 24000元" [8][V].
- Volcengine, iFlytek, SenseTime: sin precio público por minuto encontrado.
- Consolas chinas: "购买阿里云产品或服务前，必须先完成实名认证" [9][V]. Español no documentado en Tencent/Baidu/Alibaba.

**2. LLM (US$ por millón de tokens)**
- DeepSeek-flash (V4.1), fuera de pico: caché "$0.003" · entrada "$0.15" · salida "$0.6"; pico el doble [10][V]. Pico 01–04 y 06–10 UTC lun-vie = 22–01 y 03–07 en Argentina [C]. Pesos MIT [19].
- Qwen3.7-flash (Singapur, ≤32K): entrada "$0.030" · salida "$0.130" [11][V]; caché implícita "20% of the standard input token price" → 0,006 [12][V][C]. Pesos de este modelo: no confirmados.
- GLM-5.3-Flash: "GLM-5.3-Flash | $0.15 | $0.03 | Limited-time Free | $0.50" (entrada | caché | almacenamiento | salida) [14][V]; pesos MIT [19].
- MiniMax-M2.7: entrada "$0.3" · salida "$1.2" · caché "$0.06" [15][V]; pesos "NON-COMMERCIAL LICENSE" [19].
- Kimi K2.6: caché "$0.16" · entrada "$0.95" · salida "$4.00" [13][V]; pesos "modified-mit" [19].
- Gemini 3.1 Flash-Lite: entrada "$0.25" · caché "$0.025" · salida "$1.50" [16][V].
- Para autohospedar: Qwen3.8-27B, Apache-2.0, 27.800 millones de parámetros (un servidor); DeepSeek-V4.1-Flash tiene 763.000 millones (varios GPU) [19][V].

**3. Voz en español**
- TTS Qwen3-TTS-Flash-Realtime: "$0.13" por 10.000 caracteres [11][V]; voces con "Spanish" [17][V]. CosyVoice-v3-flash: "$0.13" [11][V]. MiniMax: "$60 / M characters" [15][V].
- STT qwen3-asr-flash-realtime: "$0.000090/second" [11][V]; español documentado en Qwen3-ASR-Flash [18], no en la versión realtime. GLM-ASR: "$0.0024/minute" [14][V].
- Abiertos: CosyVoice3 y Qwen3-TTS Apache-2.0 con español; Kokoro Apache-2.0 (voces "ef_dora", "em_alex"); F5-TTS CC-BY-NC y XTTS-v2 Coqui: no comerciales; Whisper-v3-turbo y faster-whisper MIT; Qwen3-ASR-0.6B Apache-2.0 con "es" [20][V].
- Avatar abierto: LiteAvatar MIT ("30fps on only CPU"), OpenAvatarChat Apache-2.0, MuseTalk MIT [21][V]. Realismo y costo de servidores: no medidos.

**4. Costo por alumno por año, US$ [C]**
Stack barato = LiveAvatar LITE + Qwen3.7-flash + Qwen3-TTS-Realtime + Qwen3-ASR-Realtime.

| Concepto | Stack previo | Stack barato | Fórmula |
|---|---|---|---|
| Solo texto | 10,2 | 0,14 (DeepSeek: 0,53) | 5,4×0,006+2,2×0,03+0,31×0,13 |
| TTS | — | 6,74 | 0,5184M×13 |
| STT | — | 2,33 | 25.920 s×0,00009 |
| Texto+voz | 27,6 | 9,21 | suma |
| Avatar, 576 min | 315,6 | 54,81 | 576×0,0792+9,21 |
| Avatar, 1.440 min | 747,6 | 123,21 | 1.440×0,0792+9,21 |
| Avatar Enterprise US$0,01/min | — | 23,61 | 1.440×0,01+9,21 |

Lo clave:
- LiveAvatar "charges per minute of session time" [1]; Anam cobra "regardless of whether you are actively speaking or not" [3]. Se pagan los 1.440 min; el estimado previo, así, da 747,6 (1.440×0,50+27,6).
- Chinos por canal: Tencent US$4.027/año [C: 27.000÷6,7046]; supuesto 72.000 min útiles/canal/año (6 h × 200 días) = 50 alumnos → US$80,5/alumno; Baidu US$71,6. Sin español documentado.
- Autohospedaje: licencias US$0; GPU y operación no calculadas.
- Datos de menores enviados al exterior: no investigado; consultar legales.

**Fuentes** (s/f = la página no muestra fecha)
[1] https://docs.liveavatar.com/docs/faq/credits.md (s/f)
[2] https://www.liveavatar.com/ (s/f)
[3] https://anam.ai/pricing (s/f)
[4] https://www.tavus.io/pricing (s/f)
[5] https://help.d-id.com/hc/en-us/articles/31262931985169-How-does-Agent-pricing-work (14-09-2025)
[6] https://help.aliyun.com/zh/avatar/avatar/product-overview/pricing (s/f)
[7] https://cloud.tencent.com/document/product/1240/101944 (17-07-2026)
[8] https://xiling.cloud.baidu.com/doc/AI_DH/s/Vlysgbz88 (12-01-2026)
[9] https://help.aliyun.com/zh/account/account-verification-overview (s/f)
[10] https://api-docs.deepseek.com/quick_start/pricing (s/f)
[11] https://www.alibabacloud.com/help/en/model-studio/model-pricing (03-10-2026)
[12] https://www.alibabacloud.com/help/en/model-studio/context-cache (28-09-2026)
[13] https://platform.moonshot.ai/docs/pricing/chat (s/f)
[14] https://docs.z.ai/guides/overview/pricing (s/f)
[15] https://platform.minimax.io/docs/guides/pricing-paygo (s/f)
[16] https://ai.google.dev/gemini-api/docs/pricing (01-10-2026)
[17] https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-list (28-09-2026)
[18] https://www.alibabacloud.com/help/en/model-studio/qwen-speech-recognition (28-09-2026)
[19] huggingface.co: deepseek-ai/DeepSeek-V4.1-Flash, Qwen/Qwen3.8-27B, zai-org/GLM-5.3-Flash, moonshotai/Kimi-K2.6, MiniMaxAI/MiniMax-M2.7
[20] huggingface.co: FunAudioLLM/Fun-CosyVoice3-0.5B-2512, Qwen/Qwen3-TTS-12Hz-1.7B-Base, hexgrad/Kokoro-82M, SWivid/F5-TTS, coqui/XTTS-v2, openai/whisper-large-v3-turbo, Systran/faster-whisper-large-v3, Qwen/Qwen3-ASR-0.6B-hf
[21] github.com: HumanAIGC/lite-avatar, HumanAIGC-Engineering/OpenAvatarChat, TMElyralab/MuseTalk
[22] https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml (02-10-2026)
