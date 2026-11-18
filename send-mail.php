<?php
header('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

function clean_text($val) {
    return trim(strip_tags((string) $val));
}

function first_post($keys, $default = '') {
    foreach ($keys as $k) {
        if (isset($_POST[$k]) && trim((string) $_POST[$k]) !== '') {
            return clean_text($_POST[$k]);
        }
    }
    return $default;
}

$name    = first_post(['name', 'fullName', 'contactName', 'modalName', 'cName'], 'Website Visitor');
$email   = filter_var(first_post(['email', 'contactEmail', 'modalEmail', 'cEmail']), FILTER_SANITIZE_EMAIL);
$phone   = first_post(['phone', 'contactPhone', 'modalPhone', 'cPhone']);
$suburb  = first_post(['suburb', 'address', 'contactAddress', 'modalAddress', 'cAddress']);
$service = first_post(['service', 'projectType', 'contactService', 'modalService'], 'Site Feasibility / Consultation');
$message = first_post(['message', 'msg', 'contactMessage', 'modalMessage', 'cMessage']);
$pageUrl = first_post(['pageUrl']);

$knownKeys = [
    'name', 'fullName', 'contactName', 'modalName', 'cName',
    'email', 'contactEmail', 'modalEmail', 'cEmail',
    'phone', 'contactPhone', 'modalPhone', 'cPhone',
    'suburb', 'address', 'contactAddress', 'modalAddress', 'cAddress',
    'service', 'projectType', 'contactService', 'modalService',
    'message', 'msg', 'contactMessage', 'modalMessage', 'cMessage',
    'pageUrl'
];

$extraLines = [];
foreach ($_POST as $k => $v) {
    if (!in_array($k, $knownKeys, true) && trim((string) $v) !== '') {
        $extraLines[] = clean_text($k) . ': ' . clean_text($v);
    }
}

$to = 'admin@intellecthomes.com.au';
$fromEmail = 'admin@intellecthomes.com.au';
$subject = 'New Website Enquiry - ' . ($name !== '' ? $name : 'Intellect Homes');
$subject = str_replace(["\r", "\n"], '', $subject);

$bodyLines = [
    "New enquiry submitted via Intellect Homes website:",
    "--------------------------------------------------",
    "Name: " . ($name ?: 'N/A'),
    "Phone: " . ($phone ?: 'N/A'),
    "Email: " . ($email ?: 'N/A'),
    "Suburb / Address: " . ($suburb ?: 'N/A'),
    "Service / Interest: " . ($service ?: 'N/A'),
    "Message:",
    ($message ?: 'No additional message provided.'),
];

if (!empty($extraLines)) {
    $bodyLines[] = "Additional Details:";
    foreach ($extraLines as $el) {
        $bodyLines[] = " - " . $el;
    }
}

if ($pageUrl !== '') {
    $bodyLines[] = "Submitted From Page: " . $pageUrl;
}

$bodyLines[] = "--------------------------------------------------";
$bodyLines[] = "Submitted at: " . date('Y-m-d H:i:s');
$body = implode("\r\n", $bodyLines);

// Backup enquiry to local log file (protected from direct web access via .htaccess)
@file_put_contents(__DIR__ . '/enquiries.log', $body . "\r\n\r\n", FILE_APPEND | LOCK_EX);

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: Intellect Homes Website <' . $fromEmail . '>',
    'Sender: ' . $fromEmail,
    'X-Mailer: PHP/' . phpversion(),
];

if ($email && filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $safeEmail = str_replace(["\r", "\n"], '', $email);
    $headers[] = 'Reply-To: ' . $safeEmail;
} else {
    $headers[] = 'Reply-To: ' . $fromEmail;
}

// Use -f envelope sender matching an existing Hostinger mailbox so Hostinger accepts & delivers it
$sent = @mail($to, $subject, $body, implode("\r\n", $headers), '-f' . $fromEmail);

echo json_encode([
    'success' => true,
    'mail_dispatched' => (bool) $sent,
    'message' => 'Thank you! Your enquiry has been received.'
]);
