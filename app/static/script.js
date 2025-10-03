// Table sorting functionality
class TableSorter {
    constructor(tableId) {
        this.table = document.getElementById(tableId);
        this.tbody = this.table.querySelector('tbody');
        this.headers = this.table.querySelectorAll('th[data-sort]');
        this.sortState = {};
        
        this.init();
    }
    
    init() {
        this.headers.forEach(header => {
            header.addEventListener('click', () => {
                this.sort(header.dataset.sort);
            });
        });
    }
    
    sort(column) {
        const isAsc = this.sortState[column] !== 'asc';
        this.sortState[column] = isAsc ? 'asc' : 'desc';
        
        // Clear other sort indicators
        this.headers.forEach(h => {
            h.classList.remove('sort-asc', 'sort-desc');
        });
        
        // Set current sort indicator
        const currentHeader = Array.from(this.headers).find(h => h.dataset.sort === column);
        if (currentHeader) {
            currentHeader.classList.add(isAsc ? 'sort-asc' : 'sort-desc');
        }
        
        // Get all rows
        const rows = Array.from(this.tbody.querySelectorAll('tr'));
        
        // Sort rows
        rows.sort((a, b) => {
            const aValue = this.getCellValue(a, column);
            const bValue = this.getCellValue(b, column);
            
            const comparison = this.compareValues(aValue, bValue);
            return isAsc ? comparison : -comparison;
        });
        
        // Re-append sorted rows
        rows.forEach(row => this.tbody.appendChild(row));
    }
    
    getCellValue(row, column) {
        const headerIndex = Array.from(this.table.querySelectorAll('th')).findIndex(
            th => th.dataset.sort === column
        );
        
        if (headerIndex === -1) return '';
        
        const cell = row.children[headerIndex];
        if (!cell) return '';
        
        return cell.textContent.trim();
    }
    
    compareValues(a, b) {
        // Try to parse as numbers
        const aNum = parseFloat(a);
        const bNum = parseFloat(b);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // String comparison
        return a.localeCompare(b);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('predictor-table');
    if (table) {
        new TableSorter('predictor-table');
    }
    
    // Add loading states and animations
    addLoadingStates();
    addTableAnimations();
    addScrollEnhancements();
});

// Add loading states for better UX
function addLoadingStates() {
    const table = document.getElementById('predictor-table');
    if (!table) return;
    
    // Add fade-in animation to table rows
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// Add table animations
function addTableAnimations() {
    const table = document.getElementById('predictor-table');
    if (!table) return;
    
    // Add hover effects
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'scale(1.01)';
            row.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'scale(1)';
            row.style.boxShadow = 'none';
        });
    });
}

// Utility functions
function formatNumber(value, decimals = 1) {
    if (value === null || value === undefined || value === '') return '';
    return parseFloat(value).toFixed(decimals);
}

function formatPercentage(value) {
    if (value === null || value === undefined || value === '') return '';
    return (parseFloat(value) * 100).toFixed(1) + '%';
}

// Add scroll enhancements
function addScrollEnhancements() {
    const tableContainer = document.querySelector('.table-container');
    if (!tableContainer) return;
    
    // Добавляем индикатор скролла под таблицей
    const scrollIndicator = document.createElement('div');
    scrollIndicator.className = 'scroll-indicator';
    scrollIndicator.innerHTML = '← Scroll horizontally to see more columns →';
    scrollIndicator.style.cssText = `
        position: absolute;
        bottom: -35px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--accent-color);
        color: white;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 500;
        opacity: 0.9;
        pointer-events: none;
        z-index: 10;
        transition: opacity 0.3s ease;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    `;
    
    // Создаем контейнер для индикатора с отступом
    const indicatorContainer = document.createElement('div');
    indicatorContainer.style.cssText = `
        position: relative;
        margin-bottom: 75px;
    `;
    
    // Вставляем контейнер после таблицы
    tableContainer.parentNode.insertBefore(indicatorContainer, tableContainer.nextSibling);
    indicatorContainer.appendChild(scrollIndicator);
    
    // Показываем/скрываем индикатор в зависимости от необходимости скролла
    function updateScrollIndicator() {
        const needsScroll = tableContainer.scrollWidth > tableContainer.clientWidth;
        scrollIndicator.style.opacity = needsScroll ? '0.9' : '0';
    }
    
    // Обновляем при изменении размера окна
    window.addEventListener('resize', updateScrollIndicator);
    updateScrollIndicator();
    
    // Скрываем индикатор при скролле
    let hideTimeout;
    tableContainer.addEventListener('scroll', () => {
        scrollIndicator.style.opacity = '0';
        clearTimeout(hideTimeout);
        hideTimeout = setTimeout(() => {
            updateScrollIndicator();
        }, 1000);
    });
}

// Export for potential use in other scripts
window.TableSorter = TableSorter;
