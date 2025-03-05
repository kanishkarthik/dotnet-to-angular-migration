import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { DynamicFormComponent } from './dynamic-form.component';

describe('DynamicFormComponent', () => {
  let component: DynamicFormComponent;
  let fixture: ComponentFixture<DynamicFormComponent>;
  let httpMock: HttpTestingController;

  const mockFormConfig = {
    sections: [
      {
        id: 'section1',
        section: 'section1',
        name: 'Test Section',
        fields: [
          {
            id: 'field1',
            name: 'Test Field',
            type: 'text',
            required: true
          }
        ]
      }
    ]
  };

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

    // Mock sessionStorage
    const mockRedirectData = {
      countryCode: 'US',
      paymentMethod: 'BKT',
      accountNumber: '12345',
      accountName: 'Test Account',
      currency: 'USD'
    };
    sessionStorage.setItem('redirectData', JSON.stringify(mockRedirectData));

    await TestBed.configureTestingModule({
      imports: [
        DynamicFormComponent,
        HttpClientTestingModule,
        ReactiveFormsModule
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DynamicFormComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    const httpRequests = httpMock.match(() => true);
    httpRequests.forEach(req => req.flush(mockFormConfig));
    httpMock.verify();
    sessionStorage.clear();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load form configuration on init', () => {
    // Handle both possible URLs
    const req = httpMock.expectOne(req => 
      req.url.includes('us_bkt.json') || req.url.includes('in_bkt.json')
    );
    expect(req.request.method).toBe('GET');
    req.flush(mockFormConfig);

    expect(component.formConfig).toBeTruthy();
    expect(component.steps.length).toBe(2); // Including review step
  });

  it('should initialize forms based on configuration', () => {
    component.formConfig = mockFormConfig;
    component.initializeForms();

    expect(component.forms['section1']).toBeTruthy();
    expect(component.forms['section1'].get('field1')).toBeTruthy();
  });

  it('should handle step navigation correctly', () => {
    // Handle HTTP request first
    const req = httpMock.expectOne(req => 
      req.url.includes('us_bkt.json') || req.url.includes('in_bkt.json')
    );
    req.flush(mockFormConfig);

    // Initialize the component state
    component.formConfig = mockFormConfig;
    component.initializeForms();
    component.steps = [...component.formConfig.sections];
    component.addReviewStep();
    component.currentStep = 0;

    // Verify initial state
    expect(component.currentStep).toBe(0);
    expect(component.isFirstStep()).toBeTrue();
    
    // Mock valid form for first step
    component.forms['section1'].get('field1')?.setValue('test');
    component.nextStep();
    
    expect(component.currentStep).toBe(1);
    expect(component.isLastStep()).toBeTrue();
  });

  it('should validate forms correctly', () => {
    component.formConfig = mockFormConfig;
    component.initializeForms();

    expect(component.isFormValid()).toBeFalsy();
    
    component.forms['section1'].get('field1')?.setValue('test');
    expect(component.isFormValid()).toBeTruthy();
  });

  it('should handle lookup modal operations', () => {
    const mockField = {
      id: 'testField',
      name: 'Test Field'
    };
    const mockSection = {
      id: 'section1',
      title: 'Test Section'
    };

    component.formConfig = mockFormConfig;
    component.initializeForms();
    component.openLookupModal(mockField, mockSection);

    expect(component.activeLookupField).toBeTruthy();
    expect(component.lookupData.length).toBeGreaterThan(0);
    expect(component.lookupHeaders.length).toBeGreaterThan(0);
  });

  it('should format data correctly for review', () => {
    component.formConfig = mockFormConfig;
    component.initializeForms();
    
    component.forms['section1'].get('field1')?.setValue('test value');
    
    const formattedData = component.getFormattedData();
    expect(formattedData.length).toBe(1);
    expect(formattedData[0].fields[0].value).toBe('test value');
  });
});
