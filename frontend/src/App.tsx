import React, { useState, useEffect } from "react";
import { Layout, Typography, Spin, Row, Col, Card, Statistic } from "antd";
import { Statistics } from "./interfaces/statistics";

const { Header, Content } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const [, setCurrentUrl] = useState<string>("Загрузка URL...");
  const [loading, setLoading] = useState<boolean>(true);
  const [statistics, setStatistics] = useState<Statistics | null>(null);

  useEffect(() => {
    const updateUrl = () => {
      chrome.storage.local.get(["url", "statistics", "loading"], (result) => {
        if (result.url) {
          setCurrentUrl(result.url);
        }
        if (result.statistics) {
          setStatistics(result.statistics);
          setLoading(false);
        }
        if (result.loading == true) {
          setLoading(true);
        } else {
          setLoading(false);
        }
      });
    };

    const handleStorageChange = (changes: { [key: string]: chrome.storage.StorageChange }) => {
      if (changes.url?.newValue) {
        setCurrentUrl(changes.url.newValue);
      }
      if (changes.statistics?.newValue) {
        setStatistics(changes.statistics.newValue);
      }
      if (changes.loading?.newValue) {
        setLoading(changes.loading.newValue);
      }
    };

    updateUrl();
    chrome.storage.onChanged.addListener(handleStorageChange);

    return () => {
      chrome.storage.onChanged.removeListener(handleStorageChange);
    };
  }, []);

  return (
    <Layout style={{ minHeight: "100%", minWidth: "95vw" }}>
      <Header>
        <Title style={{ color: "white", textAlign: "center", margin: "0 auto" }} level={3}>
          URL Scanner
        </Title>
      </Header>
      <Content style={{ padding: "10px" }}>
        {loading ? (
          <Row justify="center">
            <Spin size="large" />
          </Row>
        ) : statistics && (
          <>
            {statistics.checkPhish && (
              <Row justify="center" style={{ minWidth: "100%", marginTop: "10px" }}>
                <Col>
                  <Card title="CheckPhish">
                    <p><strong>URL:</strong> {statistics.checkPhish.url}</p>
                    <p><strong>SHA256:</strong> {statistics.checkPhish.url_sha256}</p>
                    <p><strong>Запрещено посетить:</strong> {statistics.checkPhish.resolved ? "Да" : "Нет"}</p>
                  </Card>
                </Col>
                
              </Row>
            )}
            {statistics.virusTotal && (
              <Row justify="center" style={{ minWidth: "100%", marginTop: "10px" }}>
                  <Card title="VirusTotal" style={{ minWidth: "75vw" }} >
                    <Row style={{ minWidth: "75vw", display: "flex", justifyContent: "space-around" }}>
                      <Statistic
                        title="Злонамеренный"
                        value={statistics.virusTotal.malicious}
                        valueStyle={{ color: "#cf1322" }}
                        style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
                      />
                      <Statistic
                        title="Подозрительный"
                        value={statistics.virusTotal.suspicious}
                        valueStyle={{ color: "#faad14" }}
                        style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
                      />
                    </Row>
                    <Row style={{ minWidth: "75vw", display: "flex", justifyContent: "space-around" }}>
                      <Statistic
                        title="Неизвестный"
                        value={statistics.virusTotal.undetected}
                        valueStyle={{ color: "#3f8600" }}
                        style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
                      />
                      <Statistic
                        title="Безопасный"
                        value={statistics.virusTotal.harmless}
                        valueStyle={{ color: "#52c41a" }}
                        style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
                      />
                    </Row>
                    <Row style={{ minWidth: "75vw", display: "flex", justifyContent: "space-around" }}>
                    <Statistic
                      title="Ответ не получен"
                      value={statistics.virusTotal.timeout}
                      valueStyle={{ color: "#d48806" }}
                      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
                    />
                    </Row>
                  </Card>
              </Row>
            )}
            {statistics.checkPhish && (

            <Row justify="center" style={{ marginTop: "20px" }}>
                  <img
                    src={statistics.checkPhish.image}
                    alt="URL view"
                    style={{ width: "90%" }}
                  />
                </Row>)}
            {!statistics.checkPhish && !statistics.virusTotal && (
              <Row justify="center">
                <p>Нет данных для отображения. Проверьте загрузку.</p>
              </Row>
            )}
          </>
        )}
      </Content>
    </Layout>
  );
};

export default App;
