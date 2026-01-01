# Docusaurus Integration Guide

Complete guide for integrating the RAG Chatbot widget into your Docusaurus textbook.

## Overview

The RAG Chatbot can be integrated into Docusaurus in three ways:
1. **React Component** (Recommended) - Direct integration
2. **Standalone Bundle** - Script tag inclusion
3. **Iframe Embed** - Separate deployment

---

## Method 1: React Component Integration (Recommended)

This method directly integrates the chat widget as a React component in Docusaurus.

### Step 1: Copy Files to Docusaurus

```bash
# From your project root
cp -r frontend/src/components docs/src/components/chat
cp -r frontend/src/hooks docs/src/hooks
cp -r frontend/src/services docs/src/services
cp -r frontend/src/types docs/src/types
cp frontend/src/styles/chat.css docs/src/css/chat.css
```

### Step 2: Install Dependencies

Add to your Docusaurus `package.json`:

```json
{
  "dependencies": {
    "@docusaurus/core": "^2.4.0",
    "@docusaurus/preset-classic": "^2.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

```bash
cd docs
npm install
```

### Step 3: Create Chat Component Wrapper

Create `docs/src/components/ChatbotWidget.tsx`:

```tsx
import React from 'react';
import { ChatWidget } from './chat/ChatWidget';
import '../css/chat.css';

export default function ChatbotWidget() {
  return (
    <ChatWidget
      apiBaseUrl={process.env.REACT_APP_API_URL || 'http://localhost:8000'}
      initialOpen={false}
      theme="light"
      position="bottom-right"
      maxHeight="600px"
    />
  );
}
```

### Step 4: Add to Docusaurus Theme

Edit `docs/docusaurus.config.js`:

```javascript
module.exports = {
  // ... other config
  themeConfig: {
    // ... other theme config
    navbar: {
      // ... navbar config
    },
    footer: {
      // ... footer config
    },
  },
  // Add custom fields for API URL
  customFields: {
    apiUrl: process.env.API_URL || 'http://localhost:8000',
  },
};
```

### Step 5: Add to Root Layout

Create `docs/src/theme/Root.js`:

```javascript
import React from 'react';
import ChatbotWidget from '../components/ChatbotWidget';

export default function Root({children}) {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
}
```

###Step 6: Configure Environment

Create `docs/.env`:

```bash
REACT_APP_API_URL=http://localhost:8000
```

For production, set in deployment platform:
```bash
REACT_APP_API_URL=https://your-backend-url.com
```

### Step 7: Build and Test

```bash
cd docs
npm run start  # Development
npm run build  # Production
```

Visit http://localhost:3000 - chat widget should appear!

---

## Method 2: Standalone Bundle

Build the chat widget as a standalone JavaScript bundle.

### Step 1: Create Webpack Config

Create `frontend/webpack.config.js`:

```javascript
const path = require('path');

module.exports = {
  mode: 'production',
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'chatbot.bundle.js',
    library: 'RagChatbot',
    libraryTarget: 'umd',
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  externals: {
    react: 'React',
    'react-dom': 'ReactDOM',
  },
};
```

### Step 2: Create Entry Point

Create `frontend/src/index.tsx`:

```tsx
import React from 'react';
import ReactDOM from 'react-dom';
import { ChatWidget } from './components/ChatWidget';
import './styles/chat.css';

export function initChatbot(containerId: string, options = {}) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Container #${containerId} not found`);
    return;
  }

  ReactDOM.render(
    <ChatWidget {...options} />,
    container
  );
}

// Auto-init if data attribute exists
document.addEventListener('DOMContentLoaded', () => {
  const autoInit = document.querySelector('[data-chatbot-auto-init]');
  if (autoInit) {
    const apiUrl = autoInit.getAttribute('data-api-url') || 'http://localhost:8000';
    initChatbot('chatbot-container', { apiBaseUrl: apiUrl });
  }
});

export { ChatWidget };
```

### Step 3: Build Bundle

```bash
cd frontend
npm run build  # Assumes "build": "webpack" in package.json
```

### Step 4: Include in Docusaurus

Add to `docs/static/js/chatbot.bundle.js` (copy from `frontend/dist/`)

Edit `docs/docusaurus.config.js`:

```javascript
module.exports = {
  scripts: [
    {
      src: 'https://unpkg.com/react@18/umd/react.production.min.js',
      async: false,
    },
    {
      src: 'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js',
      async: false,
    },
    {
      src: '/js/chatbot.bundle.js',
      async: true,
    },
  ],
};
```

Add to any page or `docs/src/pages/index.js`:

```html
<div id="chatbot-container" data-chatbot-auto-init data-api-url="http://localhost:8000"></div>
```

---

## Method 3: Iframe Embed

Deploy the chat widget separately and embed via iframe.

### Step 1: Deploy Frontend

Deploy `frontend/` to Vercel/Netlify/etc. as standalone React app.

### Step 2: Create Iframe Wrapper

Add to `docs/src/components/ChatbotIframe.js`:

```javascript
import React from 'react';

export default function ChatbotIframe() {
  return (
    <iframe
      src="https://your-chatbot-deploy-url.com"
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        width: '400px',
        height: '600px',
        border: 'none',
        borderRadius: '12px',
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        zIndex: 9999,
      }}
      title="Textbook Chatbot"
    />
  );
}
```

### Step 3: Add to Docusaurus

Same as Method 1 Step 5, import `ChatbotIframe` instead.

---

## Configuration Options

All methods support these `ChatWidget` props:

```typescript
interface ChatWidgetProps {
  apiBaseUrl?: string;         // Backend API URL (default: http://localhost:8000)
  initialOpen?: boolean;       // Start open? (default: false)
  theme?: 'light' | 'dark';    // Color theme (default: 'light')
  position?: 'bottom-right' | 'bottom-left';  // Position (default: 'bottom-right')
  maxHeight?: string;          // Max height (default: '600px')
  sessionId?: string;          // Custom session ID (default: auto-generated)
}
```

### Example Configurations

**Dark Theme:**
```tsx
<ChatWidget theme="dark" apiBaseUrl="https://api.example.com" />
```

**Left Position:**
```tsx
<ChatWidget position="bottom-left" />
```

**Always Open:**
```tsx
<ChatWidget initialOpen={true} maxHeight="800px" />
```

---

## Testing Integration

### 1. Test Backend Connection

Open browser console and check for errors:
- Network tab should show successful `/health` call
- No CORS errors

### 2. Test Global Query

1. Click chat widget
2. Type: "What is inverse kinematics?"
3. Send
4. Should receive answer with citations

### 3. Test Selected-Text Mode

1. Highlight text on page (at least 10 characters)
2. Click "Ask about this text" button
3. Type question
4. Send
5. Answer should reference only selected text

### 4. Test Citations

1. Click on a citation
2. Page should scroll to referenced section
3. Section should highlight briefly

---

## Troubleshooting

### Widget Not Appearing

**Check:**
- Browser console for errors
- CSS file is loaded (`chat.css`)
- Component is imported correctly
- React/ReactDOM versions match

**Fix:**
```bash
# Clear cache and rebuild
npm run clear
npm run build
```

### API Connection Fails

**Check:**
- Backend is running (`uvicorn src.main:app`)
- API URL is correct
- CORS is configured properly
- Network tab shows requests

**Fix backend CORS:**
```python
# backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add Docusaurus URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Text Selection Not Working

**Check:**
- JavaScript is enabled
- No conflicts with other selection libraries
- Console errors

**Fix:**
```tsx
// Disable if conflicts
<ChatWidget /* selection disabled temporarily */ />
```

### Styling Issues

**Check:**
- `chat.css` is imported
- CSS variables are defined
- No conflicting styles

**Fix:**
```css
/* Increase specificity */
.chat-widget.chat-widget {
  /* styles */
}
```

---

## Performance Optimization

### 1. Code Splitting

```javascript
// Lazy load chat widget
const ChatWidget = React.lazy(() => import('./components/ChatWidget'));

function App() {
  return (
    <React.Suspense fallback={<div>Loading...</div>}>
      <ChatWidget />
    </React.Suspense>
  );
}
```

### 2. Only Load on Certain Pages

```javascript
// In Root.js
import {useLocation} from '@docusaurus/router';

export default function Root({children}) {
  const location = useLocation();

  // Only show on docs pages
  const showChat = location.pathname.startsWith('/docs');

  return (
    <>
      {children}
      {showChat && <ChatbotWidget />}
    </>
  );
}
```

### 3. Defer Loading

```tsx
const [showChat, setShowChat] = useState(false);

useEffect(() => {
  // Load after page is fully loaded
  const timer = setTimeout(() => setShowChat(true), 2000);
  return () => clearTimeout(timer);
}, []);
```

---

## Deployment

### Frontend (with Docusaurus)

```bash
# Build Docusaurus with chat widget
cd docs
npm run build

# Deploy to Vercel/Netlify/GitHub Pages
# Set environment variable:
REACT_APP_API_URL=https://your-backend.com
```

### Backend Separately

See `backend/TESTING.md` for backend deployment.

---

## Example: Full Integration

Complete example with all features:

```tsx
// docs/src/components/ChatbotWidget.tsx
import React from 'react';
import { ChatWidget } from './chat/ChatWidget';
import { useColorMode } from '@docusaurus/theme-common';
import '../css/chat.css';

export default function ChatbotWidget() {
  const { colorMode } = useColorMode();

  return (
    <ChatWidget
      apiBaseUrl={process.env.REACT_APP_API_URL || 'http://localhost:8000'}
      initialOpen={false}
      theme={colorMode as 'light' | 'dark'}
      position="bottom-right"
      maxHeight="600px"
      sessionId={`user-${Date.now()}`}
    />
  );
}
```

---

## Support

If you encounter issues:

1. Check browser console for errors
2. Verify backend is running: `curl http://localhost:8000/health`
3. Test API directly: `curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d '{"query":"test"}'`
4. Review CORS configuration
5. Check React version compatibility

---

## Next Steps

1. ✅ Follow integration method above
2. ✅ Test both query modes
3. ✅ Customize styling/theme
4. ✅ Deploy backend
5. ✅ Deploy Docusaurus + chat widget
6. ✅ Monitor usage and performance