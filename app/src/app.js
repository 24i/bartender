import ReactDOM from "react-dom";
import { List } from './components/pumps';

const App = () => {

    return (
        <div className="container mx-auto pt-4">
            <h2 className="text-4xl mb-2">Pump Assignment</h2>
            <List />
        </div>
    );

};

ReactDOM.render(<App />, document.getElementById("app"));