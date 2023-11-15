package ast

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"strings"
)

func nodeToString(node ast.Node) string {
	switch x := node.(type) {
	case *ast.Ident:
		return "Ident(" + x.Name + ")"
	case *ast.BasicLit:
		return "BasicLit(" + x.Value + ")"
	case *ast.BinaryExpr:
		return "BinaryExpr(" + x.Op.String() + ")"
	case *ast.UnaryExpr:
		return "UnaryExpr(" + x.Op.String() + ")"
	case *ast.IncDecStmt:
		return "IncDecStmt(" + x.Tok.String() + ")"
	case *ast.AssignStmt:
		return "AssignStmt(" + x.Tok.String() + ")"
	default:
		return strings.Replace(fmt.Sprintf("%T", x), "*ast.", "", -1)
	}
}

func Create(code string) string {
	sb := strings.Builder{}
	fs := token.NewFileSet()

	f, err := parser.ParseFile(fs, "", code, parser.AllErrors)
	if err != nil {
		panic(err)
	}

	sb.WriteString("digraph{\n")
	parents := []*ast.Node{}
	sb.WriteString("n0x0[shape=Mdiamond, label=\"BEGIN\"]\n")
	ast.Inspect(f, func(node ast.Node) bool {
		if node != nil {
			var p *ast.Node
			if len(parents) != 0 {
				p = parents[len(parents)-1]
			}
			sb.WriteString(fmt.Sprintf("n%p->n%p\n", p, &node))
			sb.WriteString(fmt.Sprintf(`n%p[ label=%q ]`+"\n", &node, nodeToString(node)))
		}
		if node == nil {
			parents = parents[:len(parents)-1]
		} else {
			parents = append(parents, &node)
		}
		return true
	})
	sb.WriteString("}")

	return sb.String()
}
