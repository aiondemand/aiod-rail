import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ChatbotLoaderService {
  load() {
    const script = document.createElement('script');
    script.src = environment.CHATBOT_SCRIPT_SRC;
    script.defer = true;
    script.async = true;
    script.id = 'aiodbotscript';
    script.setAttribute('data-ai-endpoint', environment.CHATBOT_ENDPOINT);
    document.head.appendChild(script);
  }
}
