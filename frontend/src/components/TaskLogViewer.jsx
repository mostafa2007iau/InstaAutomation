import React, { useState } from 'react';
import { getTaskLogs } from '../services/api';

const TaskLogViewer = ({ ruleId }) => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [showLogs, setShowLogs] = useState(false);

    const fetchLogs = async () => {
        if (!showLogs) { // Only fetch if logs are hidden and we want to show them
            setLoading(true);
            try {
                const { data } = await getTaskLogs(ruleId);
                setLogs(data);
            } catch (err) {
                console.error("Failed to fetch logs", err);
            } finally {
                setLoading(false);
            }
        }
        setShowLogs(!showLogs); // Toggle visibility
    };

    return (
        <div style={{ marginTop: '10px' }}>
            <button onClick={fetchLogs}>
                {showLogs ? 'پنهان کردن گزارش' : 'نمایش گزارش عملکرد'}
            </button>
            {showLogs && (
                <div style={{ maxHeight: '200px', overflowY: 'auto', border: '1px solid #eee', padding: '10px', marginTop: '5px' }}>
                    {loading ? <p>در حال بارگذاری گزارش...</p> : (
                        logs.length > 0 ? logs.map(log => (
                            <div key={log.id} style={{ borderBottom: '1px solid #f0f0f0', padding: '5px 0', fontSize: '12px' }}>
                                <p><strong>زمان:</strong> {new Date(log.timestamp).toLocaleString('fa-IR')}</p>
                                <p><strong>توضیحات:</strong> {log.description}</p>
                                <p style={{ color: log.is_success ? 'green' : 'red' }}>
                                    <strong>وضعیت:</strong> {log.is_success ? 'موفق' : 'ناموفق'}
                                </p>
                            </div>
                        )) : <p>گزارشی برای نمایش وجود ندارد.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default TaskLogViewer;