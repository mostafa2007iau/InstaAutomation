import React, { useState, useEffect } from 'react';
import { getAutomationRules, createAutomationRule, updateAutomationRule, deleteAutomationRule } from '../services/api';
import TaskLogViewer from './TaskLogViewer';

const RuleManager = ({ post }) => {
    const [rules, setRules] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [editingRule, setEditingRule] = useState(null);

    const fetchRules = async () => {
        setLoading(true);
        try {
            const { data } = await getAutomationRules(post.pk);
            setRules(data);
        } catch (err) {
            setError('خطا در دریافت قوانین.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRules();
    }, [post]);

    const handleSaveRule = async (e) => {
        e.preventDefault();
        const ruleData = {
            post_pk: post.pk,
            post_url: `https://www.instagram.com/p/${post.code}/`,
            keywords: editingRule.keywords,
            send_comment: editingRule.send_comment,
            send_direct: editingRule.send_direct,
            comment_reply_text: editingRule.comment_reply_text,
            direct_reply_text: editingRule.direct_reply_text,
            use_ai_reply: editingRule.use_ai_reply,
            is_active: editingRule.is_active,
        };

        try {
            if (editingRule.id) {
                await updateAutomationRule(editingRule.id, ruleData);
            } else {
                await createAutomationRule(ruleData);
            }
            setEditingRule(null);
            fetchRules();
        } catch (err) {
            setError('خطا در ذخیره قانون.');
        }
    };

    const handleDeleteRule = async (ruleId) => {
        if (window.confirm('آیا از حذف این قانون مطمئن هستید؟')) {
            try {
                await deleteAutomationRule(ruleId);
                fetchRules();
            } catch (err) {
                setError('خطا در حذف قانون.');
            }
        }
    };

    const startNewRule = () => {
        setEditingRule({
            keywords: '',
            send_comment: true,
            send_direct: false,
            comment_reply_text: '',
            direct_reply_text: '',
            use_ai_reply: false,
            is_active: true,
        });
    };

    const renderRuleForm = () => (
        <form onSubmit={handleSaveRule} style={{ border: '1px solid #eee', padding: '15px', margin: '15px 0', borderRadius: '5px' }}>
            <h4>{editingRule.id ? 'ویرایش قانون' : 'قانون جدید'}</h4>

            <label>کلمات کلیدی (با کاما جدا کنید):</label>
            <input type="text" value={editingRule.keywords} onChange={(e) => setEditingRule({ ...editingRule, keywords: e.target.value })} required />

            <label><input type="checkbox" checked={editingRule.use_ai_reply} onChange={(e) => setEditingRule({ ...editingRule, use_ai_reply: e.target.checked })} /> استفاده از پاسخ هوش مصنوعی</label>

            <hr/>

            <label><input type="checkbox" checked={editingRule.send_comment} onChange={(e) => setEditingRule({ ...editingRule, send_comment: e.target.checked })} /> ارسال پاسخ به صورت کامنت</label>
            <textarea value={editingRule.comment_reply_text} onChange={(e) => setEditingRule({ ...editingRule, comment_reply_text: e.target.value })} placeholder="متن پاسخ کامنت" disabled={editingRule.use_ai_reply || !editingRule.send_comment} />

            <label><input type="checkbox" checked={editingRule.send_direct} onChange={(e) => setEditingRule({ ...editingRule, send_direct: e.target.checked })} /> ارسال پاسخ به صورت دایرکت</label>
            <textarea value={editingRule.direct_reply_text} onChange={(e) => setEditingRule({ ...editingRule, direct_reply_text: e.target.value })} placeholder="متن پاسخ دایرکت" disabled={editingRule.use_ai_reply || !editingRule.send_direct} />

            <hr/>

            <label><input type="checkbox" checked={editingRule.is_active} onChange={(e) => setEditingRule({ ...editingRule, is_active: e.target.checked })} /> فعال بودن قانون</label>

            <div style={{ marginTop: '10px' }}>
                <button type="submit">ذخیره</button>
                <button type="button" onClick={() => setEditingRule(null)}>انصراف</button>
            </div>
        </form>
    );

    const renderRuleDisplay = (rule) => (
        <div key={rule.id} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px' }}>
            <p><strong>کلمات کلیدی:</strong> {rule.keywords}</p>
            {rule.use_ai_reply ? (
                <p><strong>نوع پاسخ:</strong> هوش مصنوعی</p>
            ) : (
                <>
                    {rule.send_comment && <p><strong>پاسخ کامنت:</strong> {rule.comment_reply_text}</p>}
                    {rule.send_direct && <p><strong>پاسخ دایرکت:</strong> {rule.direct_reply_text}</p>}
                </>
            )}
            <p><strong>وضعیت:</strong> {rule.is_active ? 'فعال' : 'متوقف'}</p>
            <button onClick={() => setEditingRule(rule)}>ویرایش</button>
            <button onClick={() => handleDeleteRule(rule.id)}>حذف</button>
            <TaskLogViewer ruleId={rule.id} />
        </div>
    );

    return (
        <div>
            <h3>مدیریت قوانین برای پست: "{post.caption_text.substring(0, 50)}..."</h3>
            <button onClick={startNewRule}>ایجاد قانون جدید</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {editingRule && renderRuleForm()}
            <h4>قوانین موجود</h4>
            {loading ? <p>در حال بارگذاری...</p> : (
                rules.length > 0 ? rules.map(renderRuleDisplay) : <p>هیچ قانونی برای این پست تعریف نشده است.</p>
            )}
        </div>
    );
};

export default RuleManager;