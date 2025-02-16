// Import necessary modules
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, of } from 'rxjs';
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
    ok: () => { },
    isCancel: false
  }

  formConfig: any;
  forms: { [key: string]: FormGroup } = {};
  metaDataKey: string = '';
  activeLookupField: any;
  lookupHeaders: string[] = [];
  lookupData: any[] = [];
  currentStep: number = 0;
  steps: any[] = [];
  isStepperView: boolean = true;

  constructor(private http: HttpClient, private fb: FormBuilder) {
  }

  ngOnInit(): void {
    const redirectData = sessionStorage.getItem('redirectData');
    if (!redirectData) {
      window.location.href = '/';
    }
    const redirectDataObj = JSON.parse(redirectData || '');
    this.metaDataKey = `${redirectDataObj.countryCode.toLowerCase()}_${redirectDataObj.paymentMethod.toLowerCase()}`;

    this.loadFormConfig(this.metaDataKey).subscribe((config) => {
      if (config.status == '404') {
        const modal = this.getModal('confirmationModal');
        this.modalOptions = {
          title: 'Error',
          description: 'Failed to load data from configuration. Please try again later.',
          ok: () => {
            modal.hide();
            window.location.href = '/';
          },
          isCancel: false
        }
        modal.show();
        return;
      }
      this.formConfig = config;
      this.initializeForms();
      this.steps = this.formConfig.sections.map((section: any, index: number) => ({
        ...section,
        completed: false,
        active: index === 0
      }));
      //this.loadDataFromConfig(this.metaDataKey).subscribe((data) => {
      this.formConfig.sections.forEach((section: any) => {
        if (section.section.toLowerCase().indexOf('PaymentMethod'.toLowerCase()) !== -1) {
          section.fields.forEach((field: any) => {
            if (field.field === section.section+'_PaymentMethod') {
              field.value = redirectDataObj.paymentMethodDescription;
            } else if (field.field === section.section+'_AccountNumber') {
              field.value = redirectDataObj.accountNumber;
            } else if (field.field === section.section+'_PaymentCurrency') {
              field.value = redirectDataObj.currency;
            } else if (field.field === section.section+'_AccountName') {
              field.value = redirectDataObj.accountName;
            }
            this.forms[section.section].patchValue({ [field.field]: field.value });
          });
        }
      });
      this.addReviewStep();
      // sessionStorage.removeItem('redirectData');
      this.setFormData({});
      this.initilizeDropdownOptions({});
      // }, (error) => {

      // });
    });
  }
  setFormData(data: any) {
  }

  loadFormConfig(key: string): Observable<any> {
    return this.http.get(`/assets/metadata/${key}.json`).pipe(
      catchError((error) => {
        // Return a default value or an empty object
        return of(error);
      })
    );
  }

  loadDataFromConfig(key: string): Observable<any> {
    return this.http.get(`/assets/data/${key}.json`);
  }

  initializeForms(): void {
    this.formConfig.sections.forEach((section: any) => {
      const group: any = {};
      
      section.fields.forEach((field: any) => {
        const validators = [];
        if (field.required == "true") validators.push(Validators.required);
        if (field.pattern) validators.push(Validators.pattern(`^${field.pattern}$`));``
        if (field.maxLength) validators.push(Validators.maxLength(parseInt(field.maxLength)));
        if (field.minLength) validators.push(Validators.minLength(parseInt(field.minLength)));        
        group[field.field] = new FormControl({ value: '', disabled: field.disabled == "true" || false }, validators);
      });
      this.forms[section.section] = this.fb.group(group);
    });
  }

  isFormValid(): boolean {
    let formValid = true;
    Object.keys(this.forms).forEach((key: string) => {
      if (!this.forms[key].valid) {
        formValid = false;
      }
    });
    return formValid;
  }

  nextStep(): void {
    if (this.currentStep < this.steps.length - 1) {
      const currentSection = this.steps[this.currentStep].section;
      if (this.forms[currentSection].valid) {
        this.steps[this.currentStep].completed = true;
        this.steps[this.currentStep].active = false;
        this.currentStep++;
        this.steps[this.currentStep].active = true;
      } else {
        Object.keys(this.forms[currentSection].controls).forEach(key => {
          const control = this.forms[currentSection].get(key);
          if (control) {
            control.markAsTouched();
          }
        });
      }
    }
  }

  previousStep(): void {
    if (this.currentStep > 0) {
      this.steps[this.currentStep].active = false;
      this.currentStep--;
      this.steps[this.currentStep].active = true;
    }
  }

  canProceed(): boolean {
    if (this.currentStep >= this.steps.length) return false;
    const currentSection = this.steps[this.currentStep].section;
    return this.forms[currentSection].valid;
  }

  isLastStep(): boolean {
    return this.currentStep === this.steps.length - 1;
  }

  isFirstStep(): boolean {
    return this.currentStep === 0;
  }

  onSubmit(): void {
    if (this.isFormValid()) {
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

  getModal(id: string): any {
    const modal = new bootstrap.Modal(document.getElementById(id));
    return modal;
  }

  initilizeDropdownOptions(data: any) {
    // Initialize dropdown options based on form configuration
    this.formConfig.sections.forEach((section: any) => {
      section.fields.forEach((field: any) => {
        if (field.type === 'dropdown') {
          // if (data[field.field] && Array.isArray(data[field.field])) {
          //   field.options = this.getDropdownValues(data[field.field], field.label);
          //   return;
          // }
          field.options = this.getDropdownValues([], field.label);
        }
      });
    });
    return [];
  }

  getDropdownValues(data: [], label: string) {
    const options = [];
    options.push({ label: `--Select ${label}--`, value: '' });
    // data.forEach((item: any) => {
    //   options.push({ label: item.description, value: item.value });
    // });
    options.push({ label: 'Option 1', value: 1 });
    options.push({ label: 'Option 2', value: 2 });
    options.push({ label: 'Option 3', value: 3 });
    options.push({ label: 'Option 4', value: 4 });
    options.push({ label: 'Option 5', value: 5 });
    return options;
  }

  openLookupModal(field: any, section: string) {
    this.activeLookupField = field;
    this.activeLookupField.section = section;
    this.lookupData = [
      { name: 'Item 1', description: 'Description 1' },
      { name: 'Item 2', description: 'Description 2' },
      { name: 'Item 3', description: 'Description 3' },
      { name: 'Item 4', description: 'Description 4' },
      { name: 'Item 5', description: 'Description 5' }
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

  getFormattedData(): any[] {
    const formattedData: any[] = [];
    this.formConfig.sections.forEach((section: any) => {
      const sectionData = {
        title: section.title,
        fields: section.fields.map((field: any) => ({
          label: field.label,
          value: this.forms[section.section].get(field.field)?.value || ''
        }))
      };
      formattedData.push(sectionData);
    });
    return formattedData;
  }

  addReviewStep(): void {
    // Add review step after initialization of other steps
    this.steps.push({
      section: 'review',
      title: 'Review',
      completed: false,
      active: false
    });
  }

  goToStep(stepIndex: number): void {
    if (stepIndex < this.currentStep || this.steps[stepIndex - 1]?.completed) {
      this.steps[this.currentStep].active = false;
      this.currentStep = stepIndex;
      this.steps[this.currentStep].active = true;
    }
  }

  toggleView(): void {
    this.isStepperView = !this.isStepperView;
  }
}
