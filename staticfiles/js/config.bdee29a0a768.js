const urls = [
   'pentfinanceinc.com',
   'www.pentfinanceinc.com'
];

const URL_ROOT = urls.includes(location.hostname) ?
   'https://pentfinanceinc.com' :
   'http://localhost/bank';

const URL_PUBLIC = `${URL_ROOT}/public`;
const SITE_NAME = 'Pent Finance';