# Application Architecture Overview

This document describes the architecture and interaction between the three main components of the migration system:
1. ASP.NET MVC Application (Source)
2. Metadata Generator (Bridge)
3. Angular Application (Target)

## 1. ASP.NET MVC Application

### Structure
- Uses a configuration-driven approach for UI generation
- Implements a hierarchical view structure for different countries and payment methods
- Core components:
  - ViewConfigurations: Define field properties and validation rules
  - Controllers: Handle routing and data flow

### Key Features
- Form generation based on configurations
- Support for multiple payment methods (BKT, CBFT, DFT, RCH)
- Region-specific implementations (NAM/US, ASIA/India)

### Configuration Example
```csharp
public void ConfigurePaymentDetails()
{
    ConfigureModel(model => model.PaymentDetails.TranRefNo)
        .Name("Transaction Reference")
        .Type("textbox")
        .Required(true)
        .Pattern("[a-zA-Z0-9]+");
}
```

## 2. Metadata Generator

### Purpose
- Analyzes .NET MVC configurations
- Generates standardized metadata for Angular
- Provides API endpoints for configuration management

### Key Components
- Flask API server
- Configuration analyzer
- AI-powered metadata generation (Groq, Gemini)
- File system operations for metadata storage

### API Endpoints
```
GET  /metadata           - View metadata generation interface
POST /generate-metadata  - Generate new metadata
POST /save-metadata     - Save generated metadata
```

### Generated Metadata Structure
```json
{
  "fields": [
    {
      "id": "paymentDetails.tranRefNo",
      "name": "Transaction Reference",
      "type": "textbox",
      "required": true,
      "pattern": "[a-zA-Z0-9]+",
      "validation": {
        "messages": {
          "required": "Transaction Reference is required",
          "pattern": "Only alphanumeric characters allowed"
        }
      }
    }
  ]
}
```

## 3. Angular Application

### Architecture
- Feature-based module organization
- Dynamic form rendering based on metadata
- Reactive form implementation
- Bootstrap UI framework

### Key Features
- Dynamic component generation
- Metadata-driven form validation
- Responsive layout
- Country/Region specific routing

### Metadata Usage Example
```typescript
export class DynamicFormComponent {
  @Input() metadata: any;
  form: FormGroup;

  createForm() {
    const group = {};
    this.metadata.fields.forEach(field => {
      group[field.id] = ['', this.getValidators(field)];
    });
    this.form = this.fb.group(group);
  }
}
```

## Migration Process Flow

1. **Analyze Source**
   - Parse .NET MVC configurations
   - Extract field definitions and validation rules
   - Identify UI components and their properties

2. **Generate Metadata**
   - Convert .NET configurations to standardized JSON
   - Apply AI/ML for enhanced mapping
   - Store metadata in file system

3. **Render Angular UI**
   - Load metadata for specific route
   - Generate dynamic forms
   - Apply validation rules and UI controls

## Usage Guide

### 1. Generating Metadata
```bash
# Start metadata generator service
cd MetadataParser
python main.py

# Access web interface
open http://localhost:5000
```

### 2. Running Angular App
```bash
# Install dependencies
cd AngularApp
npm install

# Start development server
ng serve --port 5100
```

### 3. Configuration Files
- Source configurations: `/DotNetApp/ViewConfigurations/`
- Generated metadata: `/AngularApp/src/assets/metadata/`
- Migration logs: `/logs/`

## Best Practices

1. **Metadata Generation**
   - Always validate generated metadata
   - Keep original .NET configurations as reference
   - Use version control for metadata files

2. **Angular Development**
   - Follow component-based architecture
   - Implement proper error handling
   - Use TypeScript interfaces for metadata

3. **Testing**
   - Unit test metadata generation
   - Validate form behavior
   - Test across different regions/configurations
