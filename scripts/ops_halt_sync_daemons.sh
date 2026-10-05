#!/bin/bash
echo "⚠ [WARNING] Initiating total removal of Microsoft OneDrive..."

# 1. Terminating OneDrive background processes
echo "1. Terminating OneDrive background processes..."
pkill -9 OneDrive 2>/dev/null

# 2. Removing the OneDrive Application
echo "2. Removing the OneDrive Application..."
rm -rf /Applications/OneDrive.app 2>/dev/null

# 3. Eradicating hidden library files, caches, and File Provider links
echo "3. Eradicating hidden library files, caches, and File Provider links..."
rm -rf ~/Library/Application\ Support/OneDrive
rm -rf ~/Library/Application\ Support/com.microsoft.OneDrive
rm -rf ~/Library/Caches/com.microsoft.OneDrive
rm -rf ~/Library/Containers/com.microsoft.OneDrive-mac
rm -rf ~/Library/Containers/com.microsoft.OneDrive.FinderSync
rm -rf ~/Library/Group\ Containers/*.OneDriveSyncClientSuite
rm -rf ~/Library/Application\ Scripts/com.microsoft.OneDrive*
rm -rf ~/Library/Application\ Support/FileProvider/com.microsoft.OneDrive-mac.FileProvider

# 4. Remove the actual Sync folder (The ghost link in Finder)
echo "4. Deleting the local CloudStorage ghost links..."
rm -rf ~/Library/CloudStorage/OneDrive-*

echo "✅ [SUCCESS] OneDrive has been completely eradicated from this machine."
#!/bin/bash

pluginkit -r com.microsoft.OneDrive-mac.FileProvider 2>/dev/null

chflags -R nouchg ~/Library/CloudStorage/OneDrive-* 2>/dev/null

rm -rf ~/Library/CloudStorage/OneDrive-* 2>/dev/null

killall Finder

echo "✅ [SUCCESS] Locks severed and folders deleted."
