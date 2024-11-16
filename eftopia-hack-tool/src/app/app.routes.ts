import { Routes } from '@angular/router';
import { AppComponent } from './app.component';

export const routes: Routes = [
  {
    path: '',
    component: AppComponent,
    children: [
      {
        path: '',
        redirectTo: 'welcome',
        pathMatch: 'full'
      },
      {
        path: 'welcome',
        loadComponent: () => import('./welcome-page/welcome.component').then(m => m.WelcomeComponent)
      },
      {
        path: 'file-search',
        loadComponent: () => import('./file-search/file-search.component').then(m => m.FileSearchComponent)
      }
    ]
  }
];
