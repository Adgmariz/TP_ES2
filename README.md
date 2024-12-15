## Trabalho Prático: Etapa 1 - Engenharia de Software II

### Grupo:

#### Bernardo Roberto Andrade Silva
#### Alexis Duarte Guimarães Mariz

### Explicação do sistema

#### Um sistema de criação de templates e de fichas de personagens de RPG. É necessário criar um usuário para criar os templates e fichas. Um usuário cria e pode visualizar seus próprios templates, e pode criar fichas de personagens a partir deles.
#### Um template possui atributos por padrão para auxiliar na sua criação, como a lista de classes disponíveis e os templates de itens de inventário.
#### Durante a criação de uma ficha, um formulário é construído utilizando-se o template selecionado pelo usuário. Um ficha também possui atributos por padrão, como nome de personagem e experiência, além do atributo de instância do template codificado em json.

#### Há diversos testes para validação de dados na criação de um objeto "template de ficha", por exemplo para verificar se um template de item do tipo arma é um objeto json com apenas strings como chaves e com apenas os valores pré-definidos permitidos. Por exemplo:

  {"name": "", 
  "type": "", 
  "price": 0, 
  "damage": 0,
  "broken": False,
  "effects": []}
  
#### Considerando esse template de arma por exemplo, na hora de visualizar a ficha de personagem, o usuário poderia adicionar uma arma ao preencher os campos anteriores com os tipos corretos.
