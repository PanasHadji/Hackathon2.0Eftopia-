import {Component} from '@angular/core';
import {Router, RouterModule} from '@angular/router';
import {ButtonModule} from 'primeng/button';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, ButtonModule],
  template: `
    <router-outlet></router-outlet>
  `,
})
export class AppComponent {
  constructor(private router: Router) {
  }

  goToSearchPage() {
    this.router.navigate(['../file-search']);
  }
}
