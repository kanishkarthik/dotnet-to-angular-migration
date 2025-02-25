# Metadata Schema Documentation

## Overview
The metadata schema defines the structure of configuration data that bridges the .NET MVC application and Angular application. This document outlines the standard format and rules for metadata generation.

## Base Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "formId": {
      "type": "string",
      "description": "Unique identifier for the form"
    },
    "country": {
      "type": "string",
      "description": "Country code (e.g., US, India)"
    },
    "paymentMethod": {
      "type": "string",
      "enum": ["BKT", "CBFT", "DFT", "RCH"],
      "description": "Payment method identifier"
    },
    "sections": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/section"
      }
    }
  },
  "definitions": {
    "section": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/field"
          }
        }
      }
    },
    "field": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "type": {
          "type": "string",
          "enum": ["textbox", "dropdown", "date", "checkbox", "lookup", "textarea", "label"]
        },
        "required": {
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean"
        },
        "pattern": {
          "type": "string"
        },
        "maxLength": {
          "type": "integer"
        },
        "minLength": {
          "type": "integer"
        },
        "validation": {
          "type": "object",
          "properties": {
            "messages": {
              "type": "object"
            },
            "rules": {
              "type": "array"
            }
          }
        }
      }
    }
  }
}
```

## Mapping Rules

### .NET to Metadata Field Types
| .NET Type | Metadata Type | Notes |
|-----------|--------------|-------|
| textbox | textbox | Basic text input |
| label | label | Read-only text |
| lookup | lookup | With search button |
| dropdown | dropdown | Select options |
| checkbox | checkbox | Boolean input |
| textarea | textarea | Multiline text |
| date | date | Date picker |

### Validation Rules
```json
{
  "validation": {
    "messages": {
      "required": "This field is required",
      "pattern": "Invalid format",
      "maxLength": "Maximum length exceeded",
      "minLength": "Minimum length not met"
    },
    "rules": [
      {
        "type": "required",
        "value": true
      },
      {
        "type": "pattern",
        "value": "[A-Z0-9]+"
      }
    ]
  }
}
```

## Examples

### Payment Details Section
```json
{
  "formId": "US_BKT",
  "country": "US",
  "paymentMethod": "BKT",
  "sections": [
    {
      "id": "paymentDetails",
      "name": "Payment Details",
      "fields": [
        {
          "id": "tranRefNo",
          "name": "Transaction Reference",
          "type": "textbox",
          "required": true,
          "pattern": "[A-Z0-9]+",
          "maxLength": 10,
          "validation": {
            "messages": {
              "required": "Transaction reference is required",
              "pattern": "Only uppercase letters and numbers allowed"
            }
          }
        }
      ]
    }
  ]
}
```
