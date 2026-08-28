export default function GithubNoPage({ pageTitle }) {
    return (<>
    <div className="mx-4 my-4">
        <div className="text-2xl font-bold text-white">
        <h1>{pageTitle}</h1>
        </div>
        <div className="text-l text-gray-200">
            <p>This page is not available on the github page.</p>
            <p>Please <a 
                href="https://github.com/Kaiserouo/Warframe-Tools/blob/main/src/web/README.md" 
                target="_blank" 
                rel="noopener noreferrer"
                className="font-bold underline decoration-dashed underline-offset-2 hover:text-blue-400">build the project manually</a> if you want to access this function.</p>
        </div>
    </div>
    </>);
}
