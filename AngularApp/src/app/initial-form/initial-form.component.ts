import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
declare var bootstrap: any;
@Component({
  selector: 'app-initial-form',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './initial-form.component.html',
  styleUrl: './initial-form.component.scss'
})
export class InitialFormComponent {
  form: FormGroup;
  activeLookupField: any;
  lookupHeaders: string[] = [];
  lookupData: any[] = [];
  paymentMethods = [
     { name : 'Book Transfer', code: 'BKT'},
     { name : 'Cross Border Fund Transfer', code: 'CBFT'},
     { name : 'Domestic Fund Transfer', code: 'DFT'},
     { name : 'Cheque', code: 'RCH'}
  ];
  isSubmitting = false;
  constructor(private fb: FormBuilder, private router: Router) {
    this.form = this.fb.group({
      accountNumber: ['', Validators.required],
      accountName: [''],
      paymentMethodDescription: [''],
      currency: [''],
      countryCode: [''],
      paymentMethod: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.form.valid) {
      this.isSubmitting = true;
      const formValues = this.form.value;
      const redirectData = {
        accountNumber: formValues.accountNumber,
        accountName: formValues.accountName,
        paymentMethod: formValues.paymentMethod,
        paymentMethodDescription: formValues.paymentMethodDescription,
        currency: formValues.currency,
        countryCode: formValues.countryCode        
      }
      sessionStorage.setItem('redirectData', JSON.stringify(redirectData));
      
      // Simulate loading state
      setTimeout(() => {
        this.isSubmitting = false;
        this.router.navigate(['/dynamic-form']);
      }, 800);
    }
  }
  openLookupModal(field: any) {
    this.activeLookupField = field;
    // Here you would typically fetch the lookup data from a service
    this.lookupData = [
      { number: '123456', name: 'Account 1', currency: 'INR', countryCode: 'IN' },
      { number: '456789', name: 'Account 2', currency: 'USD', countryCode: 'US' },
      { number: '654321', name: 'Account 3', currency: 'INR', countryCode: 'IN' },
      { number: '987654', name: 'Account 4', currency: 'USD', countryCode: 'US' },
    ];
    this.lookupHeaders = Object.keys(this.lookupData[0]);

    const modal = new bootstrap.Modal(document.getElementById('lookupModal'));
    modal.show();
  }

  selectLookupItem(item: any) {
    if (this.activeLookupField) {
      this.form.get(this.activeLookupField)?.setValue(item.number);
      this.form.get("accountName")?.setValue(item.name);
      this.form.get("currency")?.setValue(item.currency);
      this.form.get("countryCode")?.setValue(item.countryCode);
    }
    const modal = bootstrap.Modal.getInstance(document.getElementById('lookupModal'));
    modal.hide();
  }

  onPaymentMethodChange(event: any) {
    this.form.get("paymentMethodDescription")?.setValue(event.target.selectedOptions[0].text);
  }
}
