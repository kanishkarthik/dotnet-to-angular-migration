// Import necessary modules
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
declare var bootstrap: any;
@Component({
  selector: 'app-dynamic-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './dynamic-form.component.html',
  styleUrls: ['./dynamic-form.component.scss'],
})
export class DynamicFormComponent implements OnInit {
  modalOptions = {
    title: '',
    description: '',
    ok: () => {},
    isCancel: false
  }

  formConfig: any;
  forms: { [key: string]: FormGroup } = {};
  metaDataKey: string = '';
  activeLookupField: any;
  lookupHeaders: string[] = [];
  lookupData: any[] = [];
  constructor(private http: HttpClient, private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.metaDataKey = "in_bkt";
    this.loadFormConfig(this.metaDataKey).subscribe((config) => {
      this.formConfig = config;
      this.initializeForms();
      this.loadDataFromConfig(this.metaDataKey).subscribe((data) => {
        this.setFormData(data);
        this.initilizeDropdownOptions(data);
      });
    });
  }
  setFormData(data: any) {
  }

  loadFormConfig(key: string): Observable<any> {
    return this.http.get(`/assets/metadata/${key}.json`);
  }

  loadDataFromConfig(key: string): Observable<any>{
    return this.http.get(`/assets/data/${key}.json`);
  }

  initializeForms(): void {
    this.formConfig.sections.forEach((section: any) => {
      const group: any = {};
      section.fields.forEach((field: any) => {
        const validators = [];
        if (field.required) validators.push(Validators.required);
        if (field.pattern) validators.push(Validators.pattern(`^${field.pattern}$`));
        group[field.field] = new FormControl({ value: '', disabled: field.disabled || false }, validators);
      });
      this.forms[section.section] = this.fb.group(group);
    });
  }

  isFormValid() : boolean {
    let formValid = true;
    Object.keys(this.forms).forEach((key: string) => {
        if (!this.forms[key].valid) {
            formValid = false;
        }
    });
    return formValid;
  }
  
  onSubmit(): void {
    const modal = this.getModal('confirmationModal');
    this.modalOptions = {
      title: 'Confirmation',
      description: 'The Payment has been successfully submitted',
      ok: () => {
        modal.hide();
        window.location.href = '/';
      },
      isCancel: false
    };
    modal.show();
  }

  onCancel(): void {
    const modal = this.getModal('confirmationModal');
    this.modalOptions = {
      title: 'Confirmation',
      description: 'The payment will be cancelled and will not be submitted',
      ok: () => {
        modal.hide();
        window.location.href = '/';
      },
      isCancel: true
    };
    modal.show();
  }

  getModal(id: string) : any{
    const modal = new bootstrap.Modal(document.getElementById(id));
    return modal;
  }

  initilizeDropdownOptions(data: any) {
    // Initialize dropdown options based on form configuration
    this.formConfig.sections.forEach((section: any) => {
      section.fields.forEach((field: any) => {
        if (field.type === 'dropdown') {
          if(data[field.field] && Array.isArray(data[field.field])){
            field.options = this.getDropdownValues(data[field.field], field.label);
            return;
          }
        }
      });
    });
    return [];
  }

  getDropdownValues(data: [], label: string) { 
    const options = [];
    options.push({label: `--Select ${label}--`, value: ''});
    data.forEach((item: any)=>{
      options.push({label: item.description, value: item.value});
    });
    return options;
  }

  openLookupModal(field: any, section: string) {
    this.activeLookupField = field;
    this.activeLookupField.section = section;
    // Here you would typically fetch the lookup data from a service
    this.lookupData = [
      { id: 1, name: 'Item 1', description: 'Description 1' },
      { id: 2, name: 'Item 2', description: 'Description 2' },
      // ... more items
    ];
    this.lookupHeaders = Object.keys(this.lookupData[0]);

    const modal = new bootstrap.Modal(document.getElementById('lookupModal'));
    modal.show();
  }

  selectLookupItem(item: any) {
    if (this.activeLookupField) {
      this.forms[this.activeLookupField.section.section].get(this.activeLookupField.field)?.setValue(item.name);
    }
    const modal = bootstrap.Modal.getInstance(document.getElementById('lookupModal'));
    modal.hide();
  }
}
