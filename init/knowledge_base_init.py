from neo4j import GraphDatabase
import json
import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBaseInitializer:
    def __init__(self):
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        
    def load_base_patterns(self) -> List[Dict]:
        """Load base design patterns from JSON file"""
        patterns_file = os.path.join(os.path.dirname(__file__), 'data/base_patterns.json')
        try:
            with open(patterns_file, 'r') as f:
                data = json.load(f)
                return data.get('patterns', [])
        except FileNotFoundError:
            logger.warning(f"Base patterns file not found at {patterns_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing base patterns JSON: {str(e)}")
            return []

    def init_knowledge_base(self):
        """Initialize knowledge base with design patterns and relationships"""
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )

            patterns = self.load_base_patterns()
            if not patterns:
                logger.warning("No patterns loaded from base patterns file")
                return False

            with driver.session() as session:
                # Create pattern categories
                session.run("""
                    CREATE CONSTRAINT category_name IF NOT EXISTS
                    FOR (c:Category) REQUIRE c.name IS UNIQUE
                """)
                
                session.run("""
                    MERGE (:Category {name: 'Creational'})
                    MERGE (:Category {name: 'Structural'})
                    MERGE (:Category {name: 'Behavioral'})
                """)
                
                # Create base knowledge structure
                for pattern in patterns:
                    session.run("""
                        MATCH (cat:Category {name: $category})
                        MERGE (p:Pattern {
                            name: $name,
                            description: $description
                        })
                        MERGE (p)-[:BELONGS_TO]->(cat)
                        """, 
                        category=pattern.get('category'),
                        name=pattern.get('name'),
                        description=pattern.get('description', '')
                    )
                    
                    # Add use cases if present
                    if 'use_cases' in pattern:
                        for use_case in pattern['use_cases']:
                            session.run("""
                                MATCH (p:Pattern {name: $pattern_name})
                                MERGE (u:UseCase {description: $use_case})
                                MERGE (p)-[:APPLIES_TO]->(u)
                                """,
                                pattern_name=pattern.get('name'),
                                use_case=use_case
                            )
                
                logger.info(f"Knowledge base initialized with {len(patterns)} patterns")
                return True
                
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {str(e)}")
            return False
        finally:
            if 'driver' in locals():
                driver.close()

def main():
    initializer = KnowledgeBaseInitializer()
    success = initializer.init_knowledge_base()
    
    if not success:
        logger.error("Knowledge base initialization failed")
        exit(1)

if __name__ == "__main__":
    main()
