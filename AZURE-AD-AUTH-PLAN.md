# Azure AD Authentication Implementation Plan

## Overview
Implement Azure Active Directory authentication for the security comparison site (`docsascode-security.novatrek.cc`) to provide email-based access control with a simple "Sign in with Microsoft" button.

## Current State
- **SWA**: `swa-cap-security-comparison` in `rg-cap-docs-prod`
- **Domain**: `docsascode-security.novatrek.cc` (SSL certificate provisioned)
- **Authentication**: Partially configured - app settings set, config file updated but not deployed
- **Azure AD Tenant**: `ffe15359-1529-485f-9ba2-f339d1ec58da` (`christopherblaisdellgmail.onmicrosoft.com`)
- **Azure AD App**: `1ce6c2ac-1984-41e1-98f7-f9225c301575` (created and configured)
- **Available Users**: christopher.blaisdell_gmail.com, blazeryan21_outlook.com, rblaisdell_mail.valenciacollege.edu
- **Available Groups**: "Developers" group exists

## Implementation Status

### ✅ Completed Steps

1. **Azure AD App Registration**: Created with ID `1ce6c2ac-1984-41e1-98f7-f9225c301575`
2. **App Permissions**: User.Read permission added and granted
3. **SWA App Settings**: AUTH_AAD_CLIENT_ID, AUTH_AAD_CLIENT_SECRET, AUTH_AAD_TENANT_ID configured
4. **User Invitation**: Created invitation for christopher.blaisdell@gmail.com with authenticated role
5. **Config File**: Updated `sites/security-comparison/staticwebapp.config.json` with auth routes
6. **GitHub Workflow**: Created `azure-static-web-apps-security-comparison.yml` for deployment

### ❌ Remaining Steps

1. **Deploy Config File**: The `staticwebapp.config.json` with authentication routes needs to be deployed to SWA
2. **Test Authentication**: Verify that unauthorized users are redirected to login
3. **Add Additional Users**: Invite other authorized email addresses

### Next Steps for User

To complete the authentication setup:

1. **Set GitHub Secret**: Add the deployment token as `AZURE_STATIC_WEB_APPS_API_TOKEN_SECURITY_COMPARISON` in the repository secrets
2. **Trigger Deployment**: Push a change or manually trigger the GitHub Actions workflow
3. **Test Access**: 
   - Visit `https://docsascode-security.novatrek.cc` (should redirect to Microsoft login)
   - Use the invitation URL to accept access
   - Verify authorized users can access, unauthorized users cannot

### Alternative Manual Configuration

If GitHub deployment doesn't work, manually configure routes in Azure portal:
- Navigate to SWA → Configuration → Routes
- Add route: `/*` with `allowedRoles: ["authenticated"]`

## Implementation Steps

### Step 1: Create Azure AD App Registration ✅
Create a new app registration for the security comparison site with proper redirect URIs and Microsoft Graph permissions.

**Commands**:
```bash
az ad app create --display-name "CAP Security Comparison Site" \
  --web-redirect-uris "https://docsascode-security.novatrek.cc/.auth/login/aad/callback" \
  --query appId -o tsv
```

### Step 2: Configure App Permissions
Add User.Read permission to the app registration for basic user profile access.

**Commands**:
```bash
az ad app permission add --id <APP_ID> \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope

az ad app permission grant --id <APP_ID> \
  --api 00000003-0000-0000-c000-000000000000 \
  --scope User.Read
```

### Step 3: Deploy Authentication Configuration
Use Bicep to configure SWA authentication settings with the new app registration.

**Files to create**:
- `infra/parameters/security-comparison-auth.bicepparam`
- Deploy using existing `swa-auth.bicep` module

### Step 4: Configure User Access Control
Restrict access to specific users/emails through Azure AD configuration.

**Options**:
- Individual user assignment (recommended)
- Domain-based access
- Group-based access

### Step 5: Update SWA Routes Configuration
Modify `staticwebapp.config.json` to protect routes and handle authentication redirects.

**Key changes**:
- Add `/.auth/*` route for anonymous access
- Protect `/*` route with `allowedRoles: ["authenticated"]`
- Add 401 redirect to `/.auth/login/aad`

### Step 6: Test and Validate
Verify authentication flow works correctly and users can access the site.

### Step 7: Grant Access to Specific Emails
Add desired email addresses to the allowed user list.

## Security Considerations
- Token storage handled automatically by SWA
- Configure appropriate session timeouts
- Implement proper logout flow
- Enable Azure AD sign-in logs for auditing
- Consider role-based access for future expansion

## Timeline
- App registration + basic auth: 30-45 minutes
- User access configuration: 15-30 minutes
- Testing and validation: 15-30 minutes
- **Total**: 1-2 hours

## User Experience
- Unauthenticated users see Microsoft login page
- Authenticated users access site normally
- Logout redirects to `/.auth/logout`

## Rollback Plan
If issues occur, authentication can be disabled by removing the auth configuration from SWA settings.

## Files Modified
- `sites/security-comparison/staticwebapp.config.json` (routes + auth)
- New: `infra/parameters/security-comparison-auth.bicepparam`
- New: Azure AD app registration

## Testing Checklist
- [ ] Login flow works
- [ ] Authorized users can access content
- [ ] Unauthorized users are blocked
- [ ] Logout works properly
- [ ] SSL certificate still valid
- [ ] Custom domain resolves correctly

## Decision Log
- **Authentication Provider**: Azure AD (built-in SWA support, professional)
- **User Management**: Individual user assignment (precise control, simple for small user base)
- **Access Pattern**: Email verification via Microsoft account (familiar UX)

## Last Updated
2026-03-27