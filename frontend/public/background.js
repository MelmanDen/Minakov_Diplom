chrome.tabs.onCreated.addListener(function(tab) {
    chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, updatedTab) {
        if (tabId === tab.id && changeInfo.status === 'complete' && updatedTab.url !== 'chrome://newtab/' && updatedTab.url !== 'http://chrome//startpageshared/') {
            console.log('Updated tab URL:', updatedTab.url);
            chrome.storage.local.set({ 'url': updatedTab.url });
            fetchStatistics(updatedTab.url);
            console.log('Updated URL in local storage');
            chrome.storage.local.get('url', (data) => {
                console.log('Retrieved URL from local storage:', data);
            });
        }
    });
});

const fetchStatistics = async (url) => {
    chrome.storage.local.set({ 'loading': true });

    const API_URL = "http://localhost:8000/api/v1";
    const ROUTE_NAME = "get_scan";

    try {
        const [checkPhishResponse, virusTotalResponse] = await Promise.all([
            fetch(`${API_URL}/checkphish/${ROUTE_NAME}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            }),
            fetch(`${API_URL}/virus_total/${ROUTE_NAME}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            }),
        ]);

        const checkPhishData = await checkPhishResponse.json();
        const virusTotalData = await virusTotalResponse.json();
        console.log(checkPhishData, virusTotalData);

        if (virusTotalData.malicious < 5) {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs[0]?.id) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "hideOverlay", url }, (response) => {
                        if (chrome.runtime.lastError) {
                            console.error("Error:", chrome.runtime.lastError.message);
                        } else {
                            console.log("Response from content script:", response);
                        }
                    });
                } else {
                    console.error("No active tab found");
                }
            });
        }

        const statistics = {
            checkPhish: checkPhishData.error ? null : checkPhishData,
            virusTotal: virusTotalData.error ? null : virusTotalData,
        };

        chrome.storage.local.set({ statistics });
    } catch (error) {
        console.error("Ошибка при загрузке статистики:", error);
    } finally {
        chrome.storage.local.set({ 'loading': false });
        console.log('Загрузка статистики завершена');
        
    }
};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "hideOverlay") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]?.id) {
                chrome.tabs.sendMessage(tabs[0].id, message, (response) => {
                    sendResponse(response);
                });
            } else {
                console.error("No active tab found");
            }
        });
        return true;
    }
});
