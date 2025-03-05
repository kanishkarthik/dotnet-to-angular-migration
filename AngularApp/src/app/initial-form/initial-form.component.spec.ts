import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { InitialFormComponent } from './initial-form.component';
declare var bootstrap: any;
describe('InitialFormComponent', () => {
  let component: InitialFormComponent;
  let fixture: ComponentFixture<InitialFormComponent>;
  let router: Router;

  beforeEach(async () => {
    // Mock bootstrap
    (window as any).bootstrap = {
      Modal: class {
        static getInstance() { 
          return { hide: () => {} };
        }
        show() {}
      }
    };

    await TestBed.configureTestingModule({
      imports: [InitialFormComponent, ReactiveFormsModule],
      providers: [
        {
          provide: Router,
          useValue: { navigate: jasmine.createSpy('navigate') }
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(InitialFormComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with empty form values', () => {
    expect(component.form.get('accountNumber')?.value).toBe('');
    expect(component.form.get('accountName')?.value).toBe('');
    expect(component.form.get('paymentMethod')?.value).toBe('');
  });

  it('should validate required fields', () => {
    const form = component.form;
    expect(form.valid).toBeFalsy();
    
    form.controls['accountNumber'].setValue('12345');
    form.controls['paymentMethod'].setValue('BKT');
    
    expect(form.valid).toBeTruthy();
  });

  it('should update form values when lookup item is selected', () => {
    const mockItem = {
      number: '123456',
      name: 'Test Account',
      currency: 'USD',
      countryCode: 'US'
    };

    component.activeLookupField = 'accountNumber';
    component.selectLookupItem(mockItem);

    expect(component.form.get('accountNumber')?.value).toBe('123456');
    expect(component.form.get('accountName')?.value).toBe('Test Account');
    expect(component.form.get('currency')?.value).toBe('USD');
    expect(component.form.get('countryCode')?.value).toBe('US');
  });

  it('should update payment method description on selection', () => {
    const mockEvent = {
      target: {
        selectedOptions: [{ text: 'Book Transfer' }]
      }
    };

    component.onPaymentMethodChange(mockEvent);
    expect(component.form.get('paymentMethodDescription')?.value).toBe('Book Transfer');
  });

  it('should navigate to dynamic-form on valid submission', fakeAsync(() => {
    component.form.patchValue({
      accountNumber: '12345',
      accountName: 'Test Account',
      paymentMethod: 'BKT',
      paymentMethodDescription: 'Book Transfer',
      currency: 'USD',
      countryCode: 'US'
    });

    component.onSubmit();
    tick(800);

    expect(router.navigate).toHaveBeenCalledWith(['/dynamic-form']);
    expect(sessionStorage.getItem('redirectData')).toBeTruthy();
  }));
});
