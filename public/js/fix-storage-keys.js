// One-time script to fix localStorage keys
document.addEventListener('DOMContentLoaded', function() {
    // Migrate data from old keys to new keys
    const oldKeys = {
        'babyGirlEarnedBadges': 'childrensEarnedBadges',
        'babyGirlStarCount': 'childrensStarCount'
    };
    
    let didMigrate = false;
    
    for (const [oldKey, newKey] of Object.entries(oldKeys)) {
        const oldData = localStorage.getItem(oldKey);
        if (oldData && !localStorage.getItem(newKey)) {
            localStorage.setItem(newKey, oldData);
            didMigrate = true;
        }
    }
    
    // Confirm migration (only run once)
    if (didMigrate && !localStorage.getItem('storageMigrationDone')) {
        localStorage.setItem('storageMigrationDone', 'true');
        console.log('Migrated app data from "Baby Girl" to "Children\'s Castle"');
    }
});
