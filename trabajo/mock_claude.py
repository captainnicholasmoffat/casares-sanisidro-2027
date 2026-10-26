import json, http.server, socketserver, time, sys
LOG = sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_POST(self):
        n=int(self.headers.get('content-length',0)); body=json.loads(self.rfile.read(n))
        with open(LOG,'a') as f: f.write(json.dumps({'model':body.get('model'),'system_start':body.get('system','')[:60],'n_messages':len(body.get('messages',[])),'stream':body.get('stream'),'key':self.headers.get('x-api-key'),'last_len':len(body['messages'][-1]['content'])})+'\n')
        if body.get('stream'):
            self.send_response(200); self.send_header('content-type','text/event-stream'); self.end_headers()
            txt=['Las inspecciones de comercios van a quedar grabadas. ','Sin grabación sellada, no valen el acta, la clausura ni la habilitación.\n\n','FUENTES: P1, P2\nSEGUIR: ¿Cuándo empieza? | ¿Qué más propone para los comercios?']
            self.wfile.write(b'event: message_start\ndata: {"type":"message_start"}\n\n'); self.wfile.flush()
            for t in txt:
                ev={'type':'content_block_delta','index':0,'delta':{'type':'text_delta','text':t}}
                self.wfile.write(('event: content_block_delta\ndata: '+json.dumps(ev,ensure_ascii=False)+'\n\n').encode()); self.wfile.flush(); time.sleep(0.2)
            self.wfile.write(b'event: message_delta\ndata: {"type":"message_delta","delta":{"stop_reason":"end_turn"}}\n\nevent: message_stop\ndata: {"type":"message_stop"}\n\n'); self.wfile.flush()
        else:
            out={'content':[{'type':'text','text':'¿Qué propone el programa para los comercios?'}]}
            b=json.dumps(out).encode(); self.send_response(200); self.send_header('content-type','application/json'); self.send_header('content-length',str(len(b))); self.end_headers(); self.wfile.write(b)
socketserver.ThreadingTCPServer.allow_reuse_address=True
socketserver.ThreadingTCPServer(('127.0.0.1',9911),H).serve_forever()
