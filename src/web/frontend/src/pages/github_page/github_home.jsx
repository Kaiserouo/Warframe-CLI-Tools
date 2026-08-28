
import Home from '../home.jsx';

export default function GithubHome({ setting }) {
    return (<>
        <div className="mx-4 my-4 border-2 border-gray-600 rounded-lg p-4 bg-gray-800 text-white">
            <div className="text-2xl font-bold text-white">
                <h1>Github Page Version</h1>
            </div>
            <div className="text-l text-gray-200">
                <p>This is a simplified version of Warframe Tools.</p>
                <p>Only inventory related functions are available in this version. Market related functions are not available on the github page due to the lack of API server.</p>
                <p>The data used for inventory analysis (e.g., new weapons, riven dispositions values, etc) is stored on Github repository statically, and thus may be stale. </p>
                <br />
                <p>Please <a 
                href="https://github.com/Kaiserouo/Warframe-Tools/blob/main/src/web/README.md" 
                target="_blank" 
                rel="noopener noreferrer"
                className="font-bold underline decoration-dashed underline-offset-2 hover:text-blue-400">build the project manually</a> if you want to access all functionalities.</p>
            </div>
        </div>
        <Home setting={setting} />
    </>);
}