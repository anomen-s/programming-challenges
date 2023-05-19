import { Component } from '@angular/core';

@Component({
	selector: 'app-server',
	templateUrl: './server.component.html',
	styles: [`
	    h3 {
	     color:Blue;
	    }
	    .online {
		 color:White;
	    }
	`]
})
export class ServerComponent {
  serverId = 111;
  serverStatusStr = 'off';
  
  constructor() {
   this.serverStatusStr = (Math.random() > 0.5 ? 'on' : 'off');
  }
  
  getColor() {
    return (this.serverStatusStr === 'on' ? 'green' : 'red');
  }
  
  getServerStatus() {
    return this.serverStatusStr;
  }
}
