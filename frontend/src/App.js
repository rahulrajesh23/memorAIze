import logo from './logo.svg';
import './App.css';
import { ChatScreen } from './Containers'; 
function App() {
  return (
    <div className="p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
      <ChatScreen />
    </div>
  );
}


export default App;
