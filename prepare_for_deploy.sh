#!/bin/bash

echo "Preparing deployment..."

# Check if the Flask application is running
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ | grep -q "200"; then
  echo "Flask application is running, capturing live HTML..."

  # Make sure we have the required Python packages
  pip install requests beautifulsoup4 >/dev/null 2>&1

  # Run the capture script
  python scripts/capture_live_html.py

  if [ $? -ne 0 ]; then
    echo "⚠️ Warning: Failed to capture live HTML. Falling back to template HTML creation."
    use_template_html=true
  else
    echo "✅ Successfully captured live HTML from the application!"
    use_template_html=false
  fi
else
  echo "⚠️ Warning: Flask application does not appear to be running."
  use_template_html=true
fi

echo "✅ Deployment preparation complete"