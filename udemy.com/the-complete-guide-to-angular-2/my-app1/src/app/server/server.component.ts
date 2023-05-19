import { Component } from '@angular/core';

@Component({
	selector: 'app-server',
	templateUrl: './server.component.html',
	styles: [`
	    h3 {
	     color:Blue 
	    }
	`]
})
export class ServerComponent {
  serverId = 111;
  serverStatusStr = 'off';
  
  getServerStatus() {
    return this.serverStatusStr;
  }
}
