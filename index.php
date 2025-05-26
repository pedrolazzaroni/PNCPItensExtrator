<?php
// Configuração do banco de dados
$host = 'localhost';
$user = 'root';
$password = '';
$database = 'ataspncp';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$database;charset=utf8mb4", $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Erro na conexão: " . $e->getMessage());
}

// Parâmetros de pesquisa
$search = isset($_GET['search']) ? $_GET['search'] : '';
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 50; // Itens por página
$offset = ($page - 1) * $limit;

// Query base
$whereClause = '';
$params = [];

if (!empty($search)) {
    $whereClause = "WHERE descricao LIKE :search OR numero LIKE :search OR nomeOrgao LIKE :search OR numeroControlePNCPCompra LIKE :search";
    $params[':search'] = "%$search%";
}

// Conta total de registros
$countSql = "SELECT COUNT(*) FROM atas_itens_pncp $whereClause";
$countStmt = $pdo->prepare($countSql);
$countStmt->execute($params);
$totalRecords = $countStmt->fetchColumn();
$totalPages = ceil($totalRecords / $limit);

// Busca os registros
$sql = "SELECT * FROM atas_itens_pncp $whereClause ORDER BY id DESC LIMIT :limit OFFSET :offset";
$stmt = $pdo->prepare($sql);

// Adiciona parâmetros de paginação
$params[':limit'] = $limit;
$params[':offset'] = $offset;

foreach ($params as $key => $value) {
    if ($key === ':limit' || $key === ':offset') {
        $stmt->bindValue($key, $value, PDO::PARAM_INT);
    } else {
        $stmt->bindValue($key, $value);
    }
}

$stmt->execute();
$itens = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Itens PNCP - Atas de Registro de Preço</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .search-bar {
            padding: 20px;
            background: #ecf0f1;
            border-bottom: 1px solid #ddd;
        }

        .search-form {
            display: flex;
            gap: 10px;
            max-width: 600px;
            margin: 0 auto;
        }

        .search-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }

        .search-btn {
            padding: 12px 24px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }

        .search-btn:hover {
            background: #2980b9;
        }

        .clear-btn {
            padding: 12px 24px;
            background: #95a5a6;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            font-size: 16px;
        }

        .clear-btn:hover {
            background: #7f8c8d;
        }

        .stats {
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
            color: #2c3e50;
        }

        .table-container {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            font-size: 14px;
        }

        th {
            background: #34495e;
            color: white;
            font-weight: bold;
            position: sticky;
            top: 0;
        }

        tr:nth-child(even) {
            background: #f8f9fa;
        }

        tr:hover {
            background: #e8f4f8;
        }

        .description {
            max-width: 300px;
            word-wrap: break-word;
        }

        .valor {
            text-align: right;
            font-weight: bold;
            color: #27ae60;
        }

        .pagination {
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
        }

        .pagination a, .pagination span {
            display: inline-block;
            padding: 8px 12px;
            margin: 0 5px;
            border: 1px solid #ddd;
            text-decoration: none;
            color: #333;
            border-radius: 4px;
        }

        .pagination a:hover {
            background: #3498db;
            color: white;
        }

        .pagination .current {
            background: #3498db;
            color: white;
        }

        .no-results {
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-size: 18px;
        }        .orgao {
            font-size: 12px;
            color: #7f8c8d;
        }

        .btn-edital {
            padding: 6px 12px;
            background: #e74c3c;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            transition: background 0.3s;
        }

        .btn-edital:hover {
            background: #c0392b;
            color: white;
        }

        .btn-edital:target {
            color: white;
        }

        @media (max-width: 768px) {
            .search-form {
                flex-direction: column;
            }
            
            th, td {
                padding: 8px;
                font-size: 12px;
            }
            
            .description {
                max-width: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-bar">
            <form method="GET" class="search-form">                <input 
                    type="text" 
                    name="search" 
                    class="search-input" 
                    value="<?php echo htmlspecialchars($search); ?>"
                >
                <button type="submit" class="search-btn">Buscar</button>
                <a href="?" class="clear-btn">Limpar</a>
            </form>
        </div>        <div class="stats">
            Total de registros encontrados: <?php echo number_format($totalRecords, 0, ',', '.'); ?>
            <?php if (!empty($search)): ?>
                | Pesquisando por: "<?php echo htmlspecialchars($search); ?>"
            <?php endif; ?>
        </div>

        <div class="table-container">
            <?php if (count($itens) > 0): ?>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nº Item</th>
                            <th>Descrição</th>
                            <th>Quantidade</th>
                            <th>Valor Unitário</th>
                            <th>Valor Total</th>                            <th>Órgão</th>
                            <th>Nº Controle</th>
                            <th>Data Inclusão</th>
                            <th>Edital</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($itens as $item): ?>
                            <tr>
                                <td><?php echo $item['id']; ?></td>
                                <td><?php echo htmlspecialchars($item['numero']); ?></td>
                                <td class="description"><?php echo htmlspecialchars($item['descricao']); ?></td>
                                <td><?php echo htmlspecialchars($item['quantidade']); ?></td>
                                <td class="valor"><?php echo htmlspecialchars($item['valor_unitario']); ?></td>
                                <td class="valor"><?php echo htmlspecialchars($item['valor_total']); ?></td>
                                <td class="orgao">
                                    <?php echo htmlspecialchars($item['nomeOrgao']); ?>
                                </td>
                                <td>
                                    <small><?php echo htmlspecialchars($item['numeroControlePNCPCompra']); ?></small>
                                </td>                                <td>
                                    <?php 
                                    if ($item['dataInclusao']) {
                                        echo date('d/m/Y', strtotime($item['dataInclusao']));
                                    }
                                    ?>
                                </td>
                                <td>
                                    <?php 
                                    // Gera o link do edital baseado no numeroControlePNCPCompra
                                    if ($item['numeroControlePNCPCompra']) {
                                        // Extrai informações do número de controle: CNPJ-digito-numero/ano
                                        if (preg_match('/(\d+)-\d+-(\d+)\/(\d+)/', $item['numeroControlePNCPCompra'], $matches)) {
                                            $cnpj = $matches[1];
                                            $edital = $matches[2];
                                            $ano = $matches[3];
                                            $url_edital = "https://pncp.gov.br/app/editais/{$cnpj}/{$ano}/" . intval($edital);
                                            echo "<a href='{$url_edital}' target='_blank' class='btn-edital'>🔗 Ver Edital</a>";
                                        } else {
                                            echo "<span style='color: #7f8c8d; font-size: 12px;'>N/A</span>";
                                        }
                                    } else {
                                        echo "<span style='color: #7f8c8d; font-size: 12px;'>N/A</span>";
                                    }
                                    ?>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <div class="no-results">
                    Nenhum resultado encontrado
                    <?php if (!empty($search)): ?>
                        para "<?php echo htmlspecialchars($search); ?>"
                    <?php endif; ?>
                </div>
            <?php endif; ?>
        </div>

        <?php if ($totalPages > 1): ?>
            <div class="pagination">
                <?php
                // Botão anterior
                if ($page > 1): ?>
                    <a href="?page=<?php echo $page-1; ?><?php echo !empty($search) ? '&search='.urlencode($search) : ''; ?>">« Anterior</a>
                <?php endif;

                // Páginas
                $start = max(1, $page - 2);
                $end = min($totalPages, $page + 2);

                if ($start > 1): ?>
                    <a href="?page=1<?php echo !empty($search) ? '&search='.urlencode($search) : ''; ?>">1</a>
                    <?php if ($start > 2): ?>
                        <span>...</span>
                    <?php endif;
                endif;

                for ($i = $start; $i <= $end; $i++):
                    if ($i == $page): ?>
                        <span class="current"><?php echo $i; ?></span>
                    <?php else: ?>
                        <a href="?page=<?php echo $i; ?><?php echo !empty($search) ? '&search='.urlencode($search) : ''; ?>"><?php echo $i; ?></a>
                    <?php endif;
                endfor;

                if ($end < $totalPages): ?>
                    <?php if ($end < $totalPages - 1): ?>
                        <span>...</span>
                    <?php endif; ?>
                    <a href="?page=<?php echo $totalPages; ?><?php echo !empty($search) ? '&search='.urlencode($search) : ''; ?>"><?php echo $totalPages; ?></a>
                <?php endif;

                // Botão próximo
                if ($page < $totalPages): ?>
                    <a href="?page=<?php echo $page+1; ?><?php echo !empty($search) ? '&search='.urlencode($search) : ''; ?>">Próximo »</a>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>