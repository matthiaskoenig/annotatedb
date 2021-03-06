/**
 * Helpers to work with icons.
 */

const icons_table = {
    home: 'fas fa-home',
    references: 'fas fa-file-alt',
    reference: 'fas fa-file-alt',
    about: 'fas fa-info-circle',
    api: 'fas fa-code',
    admin: 'fas fa-cogs',
    account: 'fas fa-user-circle',
    github: 'fab fa-github',
    files: 'fas fa-file',
    file: 'fas fa-file',
    file_excel: 'fas fa-file-excel',
    file_image: 'fas fa-file-image',
    file_csv: 'fas fa-file-csv',
    file_pdf: 'fas fa-file-pdf',
    previous:'fas fa-arrow-left',
    next:'fas fa-arrow-right',
    star:'fas fa fa-star',
    warning:'fas fa-exclamation-triangle',
    private:'fas fa-lock',
    public:'fas fa-lock-open',
    closed:'fab fa-creative-commons-pd',
    open:'fab fa-creative-commons-pd-alt',
    na:'fas fa-ban',
    success:'fas fa-check-circle',
};


function lookup_icon(key){
    return icons_table[key]
}

export {lookup_icon};