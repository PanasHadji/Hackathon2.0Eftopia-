import {Component} from '@angular/core';
import {Router, RouterModule} from '@angular/router';
import {ButtonModule} from 'primeng/button';
import {BrowserAnimationsModule, NoopAnimationsModule} from '@angular/platform-browser/animations';

@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [RouterModule, ButtonModule],
  template: `
    <div class="main-container">
      <h1 class="animated-title">Enhancing Digital Justice</h1>
      <button pButton type="button" label="Start" class="start-button" (click)="goToSearchPage()"></button>
    </div>
  `,
  styles: [`
    .main-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    .animated-title {
      font-size: 4rem;
      color: white;
      animation: fadeIn 2s ease-in-out;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }

    .start-button {
      margin-top: 20px;
    }
  `]
})
export class WelcomeComponent {
  constructor(private router: Router) {
  }

  goToSearchPage() {
    this.router.navigate(['./file-search']);
  }
}
