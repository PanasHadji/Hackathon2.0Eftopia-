import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {DropdownModule} from 'primeng/dropdown';
import {CalendarModule} from 'primeng/calendar';
import {ButtonModule} from 'primeng/button';
import {InputTextModule} from 'primeng/inputtext';
import {TooltipModule} from 'primeng/tooltip';
import {InputTextareaModule} from 'primeng/inputtextarea';
import {MultiSelectModule} from 'primeng/multiselect';

@Component({
  selector: 'app-file-search',
  standalone: true,
  templateUrl: './file-search.component.html',
  styleUrls: ['./file-search.component.scss', 'layout.css'],
  imports: [
    CommonModule,
    FormsModule,
    DropdownModule,
    CalendarModule,
    ButtonModule,
    InputTextModule,
    TooltipModule,
    InputTextareaModule,
    MultiSelectModule,
  ]
})
export class FileSearchComponent {
  searchQuery: string = '';
  searchCAseDetailsQuery: string = '';
  selectedLanguage: any;
  selectedCourt: any;
  startDate: Date | null = null;
  endDate: Date | null = null
  article: string = '';
  displayInfo: boolean = false;

  languages = [{name:'English'}, {name:'Greek'}, {name:'French'}];
  courts = [{name:'Court 1'}, {name:'Court 2'}, {name:'Court 3'}];

  onSearch() {
    console.log('Searching for:', this.searchQuery);
  }

  showInfo() {
    this.displayInfo = true;
  }
}
