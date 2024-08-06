import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QSizePolicy
)
from sqlalchemy.orm import Session
from config import User, SessionLocal
from schema import UserCreate

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciador de Senhas')
        self.setGeometry(100, 100, 650, 450)
        self.layout = QVBoxLayout()

        # Dados de paginação
        self.current_page = 1
        self.rows_per_page = 10

        # Entrada de Plataforma, Usuario e Senha
        self.plataforma_input = QLineEdit(placeholderText="Plataforma")
        self.usuario_input = QLineEdit(placeholderText="Usuario")
        self.senha_input = QLineEdit(placeholderText="Senha")

        # Botões
        self.add_button = QPushButton('Adicionar')
        self.edit_button = QPushButton('Editar')
        self.delete_button = QPushButton('Remover')

        # Tabela para exibir usuários
        self.users_table = QTableWidget(0, 4)
        self.users_table.setHorizontalHeaderLabels(['ID', 'Plataforma', 'Usuario', 'Senha'])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout para os botões
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        # Campo e botão de busca
        self.search_input = QLineEdit(self, placeholderText="Buscar por plataforma...")
        self.search_button = QPushButton('Buscar', self)
        self.search_button.clicked.connect(self.search_register)

        # Adicionando campo e botão de busca ao layout
        search_layout = QHBoxLayout()
        self.layout.addWidget(QLabel('Buscar por plataforma:'))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        self.layout.insertLayout(4, search_layout)  # Insere o layout de busca na posição desejada

        # Adicionando widgets ao layout principal
        self.layout.addWidget(QLabel('Plataforma:'))
        self.layout.addWidget(self.plataforma_input)
        self.layout.addWidget(QLabel('Usuario:'))
        self.layout.addWidget(self.usuario_input)
        self.layout.addWidget(QLabel('Senha:'))
        self.layout.addWidget(self.senha_input)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.users_table)

        # Adiciona controles de paginação
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton('Anterior')
        self.next_button = QPushButton('Próximo')
        self.page_label = QLabel()

        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)
        self.layout.addLayout(self.pagination_layout)

        # Conecta os botões de paginação
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        self.setLayout(self.layout)

        # Conectando sinais
        self.add_button.clicked.connect(self.add_register)
        self.edit_button.clicked.connect(self.edit_register)
        self.delete_button.clicked.connect(self.delete_register)

        self.load_registers()

        # Aplicando estilos CSS
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Verde */
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Verde mais claro */
            }
            QPushButton:pressed {
                background-color: #397d3f; /* Verde mais escuro */
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QTableWidget {
                gridline-color: #d3d3d3; /* Cor das linhas da grade */
                background-color: #f5f5f5; /* Cor de fundo */
                border-radius: 5px;
            }
            QTableWidget::item {
                border: 1px solid #d3d3d3;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50; /* Cor de seleção */
                color: white;
            }
            QHeaderView::section {
                background-color: #4CAF50; /* Cor do cabeçalho */
                color: white;
                padding: 5px;
                border: none;
            }
        """)

    def add_register(self):
        session = SessionLocal()
        try:
            user_data = UserCreate(
                plataforma=self.plataforma_input.text(), 
                usuario=self.usuario_input.text(), 
                senha=self.senha_input.text()
            )
            new_user = User(plataforma=user_data.plataforma, usuario=user_data.usuario, senha=user_data.senha)
            session.add(new_user)
            session.commit()
            self.load_registers()
            self.plataforma_input.clear()
            self.usuario_input.clear()
            self.senha_input.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Erro', str(e))
        finally:
            session.close()

    def search_register(self):
        self.current_page = 1
        self.load_registers()

    def load_registers(self):
        session = SessionLocal()
        term = self.search_input.text().strip()
        query = session.query(User)

        if term:
            query = query.filter(User.plataforma.like(f"%{term}%"))

        users = query.all()

        total_rows = len(users)
        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page
        paginated_users = users[start_index:end_index]

        self.users_table.setRowCount(0)  # Limpa a tabela antes de adicionar novas linhas
        for user in paginated_users:
            row_position = self.users_table.rowCount()
            self.users_table.insertRow(row_position)
            self.users_table.setItem(row_position, 0, QTableWidgetItem(str(user.id)))
            self.users_table.setItem(row_position, 1, QTableWidgetItem(user.plataforma))
            self.users_table.setItem(row_position, 2, QTableWidgetItem(user.usuario))
            self.users_table.setItem(row_position, 3, QTableWidgetItem(user.senha))

        session.close()
        
        # Atualiza o rótulo de paginação
        total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page
        self.page_label.setText(f"Página {self.current_page} de {total_pages}")
        
        # Habilita/desabilita botões de navegação
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_registers()

    def next_page(self):
        session = SessionLocal()
        term = self.search_input.text().strip()
        query = session.query(User)

        if term:
            query = query.filter(User.plataforma.like(f"%{term}%"))

        total_rows = query.count()
        session.close()

        total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page

        if self.current_page < total_pages:
            self.current_page += 1
            self.load_registers()

    def edit_register(self):
        selected_items = self.users_table.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            user_id = str(self.users_table.item(selected_row, 0).text())

            # Carrega o usuário do banco de dados
            session = SessionLocal()
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                # Atualiza os dados do usuário
                try:
                    user_data = UserCreate(
                        plataforma=self.plataforma_input.text(), 
                        usuario=self.usuario_input.text(), 
                        senha=self.senha_input.text()
                    )
                    user.plataforma = user_data.plataforma
                    user.usuario = user_data.usuario
                    user.senha = user_data.senha
                    session.commit()
                    QMessageBox.information(self, 'Sucesso', 'Registro atualizado com sucesso!')
                    self.plataforma_input.clear()
                    self.usuario_input.clear()
                    self.senha_input.clear()
                except Exception as e:
                    session.rollback()
                    QMessageBox.critical(self, 'Erro', str(e))
                finally:
                    session.close()
                    self.load_registers()
        else:
            QMessageBox.warning(self, 'Seleção', 'Por favor, selecione uma plataforma para editar.')

    def delete_register(self):
        selected_items = self.users_table.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            user_id = int(self.users_table.item(selected_row, 0).text())

            reply = QMessageBox.question(self, 'Confirmar', 'Você tem certeza que deseja remover este registro?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                session = SessionLocal()
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    try:
                        session.delete(user)
                        session.commit()
                        QMessageBox.information(self, 'Sucesso', 'Registro removido com sucesso!')
                    except Exception as e:
                        session.rollback()
                        QMessageBox.critical(self, 'Erro', str(e))
                    finally:
                        session.close()
                        self.load_registers()
        else:
            QMessageBox.warning(self, 'Seleção', 'Por favor, selecione um registro para remover.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
