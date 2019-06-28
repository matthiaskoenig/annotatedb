import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'

Vue.config.productionTip = false



/** --------------------------------------------------------------
 *  FontAwesome
 *  -------------------------------------------------------------- */
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome';

import { faCoffee, faFileAlt, faUser, faUsers, faFemale, faMale, faCapsules, faProcedures, faFileMedical,
  faFileMedicalAlt, faShareSquare, faChartLine, faChartBar, faInfoCircle, faCode, faLaptopCode, faTablet, faTablets,
  faCube, faCubes, faUserCog, faUserEdit, faEnvelope, faTicketAlt, faCheckCircle, faTimesCircle, faBookReader, faTrashAlt,
  faCommentAlt, faAlignLeft, faFileExcel, faFileCsv, faFilePdf
} from '@fortawesome/free-solid-svg-icons';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

library.add(faCoffee, faFileAlt, faUser, faUsers, faFemale, faMale, faCapsules, faProcedures, faFileMedical, faFileMedicalAlt,
    faShareSquare, faChartLine, faChartBar, faInfoCircle, faGithub, faCode, faLaptopCode, faTablet, faTablets, faCube, faCubes,
    faUserCog, faUserEdit, faEnvelope, faTicketAlt, faCheckCircle, faTimesCircle, faBookReader, faTrashAlt, faCommentAlt,
    faAlignLeft, faFileExcel, faFileCsv, faFilePdf);

Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);




new Vue({
  render: h => h(App),
}).$mount('#app')
