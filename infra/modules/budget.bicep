// ===========================================================================
// Azure Budget Alert — NovaTrek
// Monthly spending alerts to prevent runaway costs.
// ===========================================================================

@description('Environment identifier')
param environment string

@description('Monthly budget amount in USD')
param amount int = 50

@description('Email addresses for budget notifications')
param contactEmails array = ['architect@novatrek.example.com']

@description('Budget start date (first of current month, ISO 8601)')
param startDate string

// ---------------------------------------------------------------------------
// Budget
// ---------------------------------------------------------------------------

resource budget 'Microsoft.Consumption/budgets@2023-11-01' = {
  name: 'budget-novatrek-${environment}'
  properties: {
    category: 'Cost'
    amount: amount
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: startDate
    }
    notifications: {
      actual80: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 80
        contactEmails: contactEmails
      }
      actual100: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 100
        contactEmails: contactEmails
      }
      forecast120: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 120
        thresholdType: 'Forecasted'
        contactEmails: contactEmails
      }
    }
  }
}
