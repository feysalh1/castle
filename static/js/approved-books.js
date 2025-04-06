// Approved Books management for parent dashboard
document.addEventListener('DOMContentLoaded', function() {
    const childSelect = document.getElementById('approve-books-child-select');
    const booksContainer = document.querySelector('.available-books-container');
    const noChildSelected = document.querySelector('.no-child-selected');
    const booksGrid = document.querySelector('.books-grid');
    const ageGroupFilter = document.getElementById('book-age-filter');
    const approveButton = document.getElementById('approve-selected-books');
    const unapproveButton = document.getElementById('unapprove-selected-books');
    
    let currentChildId = null;
    let allBooks = [];
    
    // Handle child selection
    if (childSelect) {
        childSelect.addEventListener('change', function() {
            const childId = this.value;
            currentChildId = childId;
            
            if (childId) {
                // Show books container and hide no child message
                booksContainer.style.display = 'block';
                noChildSelected.style.display = 'none';
                
                // Load books for this child
                loadChildBooks(childId);
            } else {
                // Hide books container and show no child message
                booksContainer.style.display = 'none';
                noChildSelected.style.display = 'block';
                booksGrid.innerHTML = '<div class="loading-books">Select a child to view books</div>';
            }
        });
    }
    
    // Handle age group filter
    if (ageGroupFilter) {
        ageGroupFilter.addEventListener('change', function() {
            filterBooks();
        });
    }
    
    // Handle approve button
    if (approveButton) {
        approveButton.addEventListener('click', function() {
            if (!currentChildId) return;
            
            const selectedBooks = getSelectedBookIds();
            if (selectedBooks.length === 0) {
                showMessage('Please select at least one book to approve', 'error');
                return;
            }
            
            approveBooks(currentChildId, selectedBooks);
        });
    }
    
    // Handle unapprove button
    if (unapproveButton) {
        unapproveButton.addEventListener('click', function() {
            if (!currentChildId) return;
            
            const selectedBooks = getSelectedBookIds();
            if (selectedBooks.length === 0) {
                showMessage('Please select at least one book to remove approval', 'error');
                return;
            }
            
            unapproveBooks(currentChildId, selectedBooks);
        });
    }
    
    // Function to load books for a child
    function loadChildBooks(childId) {
        booksGrid.innerHTML = '<div class="loading-books">Loading books...</div>';
        
        // Make API request to get books
        fetch(`/api/books/get-child-approved?child_id=${childId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load books');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    allBooks = data.books;
                    renderBooks(allBooks);
                } else {
                    showMessage(data.message || 'Failed to load books', 'error');
                    booksGrid.innerHTML = '<div class="error-message">Failed to load books</div>';
                }
            })
            .catch(error => {
                console.error('Error loading books:', error);
                booksGrid.innerHTML = '<div class="error-message">Error loading books</div>';
            });
    }
    
    // Function to render books in the grid
    function renderBooks(books) {
        if (books.length === 0) {
            booksGrid.innerHTML = '<div class="empty-message">No books found</div>';
            return;
        }
        
        let html = '';
        books.forEach(book => {
            const isApproved = book.is_approved ? 'approved' : '';
            html += `
                <div class="book-card ${isApproved}" data-book-id="${book.id}" data-age-group="${book.age_group.id}">
                    <div class="book-selection">
                        <input type="checkbox" id="book-${book.id}" class="book-select-checkbox">
                    </div>
                    <div class="book-info">
                        <h4>${book.title}</h4>
                        <p class="book-description">${book.description || 'No description available'}</p>
                        <div class="book-meta">
                            <span class="age-group">Age Group: ${book.age_group.name}</span>
                            <span class="difficulty">Difficulty: ${book.difficulty_level}</span>
                            <span class="reading-time">Reading Time: ${book.reading_time_minutes} mins</span>
                        </div>
                        <div class="book-status">
                            ${book.is_approved ? 
                                '<span class="approved-badge">Approved</span>' : 
                                '<span class="not-approved-badge">Not Approved</span>'}
                        </div>
                    </div>
                </div>
            `;
        });
        
        booksGrid.innerHTML = html;
        
        // Add click handler for book cards
        const bookCards = document.querySelectorAll('.book-card');
        bookCards.forEach(card => {
            card.addEventListener('click', function(e) {
                // Don't toggle if clicking on the checkbox itself
                if (e.target.type !== 'checkbox') {
                    const checkbox = this.querySelector('.book-select-checkbox');
                    checkbox.checked = !checkbox.checked;
                }
            });
        });
    }
    
    // Function to filter books by age group
    function filterBooks() {
        const ageGroupId = ageGroupFilter.value;
        
        if (ageGroupId === 'all') {
            renderBooks(allBooks);
        } else {
            const filteredBooks = allBooks.filter(book => 
                book.age_group.id.toString() === ageGroupId
            );
            renderBooks(filteredBooks);
        }
    }
    
    // Function to get selected book IDs
    function getSelectedBookIds() {
        const checkboxes = document.querySelectorAll('.book-select-checkbox:checked');
        return Array.from(checkboxes).map(cb => 
            parseInt(cb.closest('.book-card').dataset.bookId)
        );
    }
    
    // Function to approve books
    function approveBooks(childId, bookIds) {
        fetch('/api/books/approve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                child_id: childId,
                book_ids: bookIds
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to approve books');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showMessage(data.message || 'Books approved successfully', 'success');
                loadChildBooks(childId); // Reload the books to show updated status
            } else {
                showMessage(data.message || 'Failed to approve books', 'error');
            }
        })
        .catch(error => {
            console.error('Error approving books:', error);
            showMessage('Error approving books', 'error');
        });
    }
    
    // Function to unapprove books
    function unapproveBooks(childId, bookIds) {
        fetch('/api/books/unapprove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                child_id: childId,
                book_ids: bookIds
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to remove book approvals');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showMessage(data.message || 'Book approvals removed successfully', 'success');
                loadChildBooks(childId); // Reload the books to show updated status
            } else {
                showMessage(data.message || 'Failed to remove book approvals', 'error');
            }
        })
        .catch(error => {
            console.error('Error removing book approvals:', error);
            showMessage('Error removing book approvals', 'error');
        });
    }
    
    // Helper function to show messages
    function showMessage(message, type = 'info') {
        // Check if we have a flash messages container
        let flashContainer = document.querySelector('.flash-messages');
        
        // Create it if it doesn't exist
        if (!flashContainer) {
            flashContainer = document.createElement('div');
            flashContainer.className = 'flash-messages';
            document.querySelector('main').prepend(flashContainer);
        }
        
        // Create the message element
        const msgElement = document.createElement('div');
        msgElement.className = `flash ${type}`;
        msgElement.textContent = message;
        
        // Add it to the container
        flashContainer.appendChild(msgElement);
        
        // Remove it after 5 seconds
        setTimeout(() => {
            msgElement.remove();
        }, 5000);
    }
});
