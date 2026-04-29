import './style.css';
import { App } from './ui/App';

const root = document.querySelector<HTMLDivElement>('#app')!;
const app = new App();
app.mount(root);
