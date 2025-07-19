from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator

metamodel_version = "None"
version = "1.0.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_prefix": "http://schema.repronim.org/",
        "default_range": "string",
        "id": "http://schema.repronim.org/",
        "imports": ["linkml:types"],
        "name": "reproschema",
        "prefixes": {
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            },
            "nidm": {
                "prefix_prefix": "nidm",
                "prefix_reference": "http://purl.org/nidash/nidm#",
            },
            "owl": {
                "prefix_prefix": "owl",
                "prefix_reference": "http://www.w3.org/2002/07/owl#",
            },
            "prov": {
                "prefix_prefix": "prov",
                "prefix_reference": "http://www.w3.org/ns/prov#",
            },
            "rdf": {
                "prefix_prefix": "rdf",
                "prefix_reference": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            },
            "rdfs": {
                "prefix_prefix": "rdfs",
                "prefix_reference": "http://www.w3.org/2000/01/rdf-schema#",
            },
            "reproschema": {
                "prefix_prefix": "reproschema",
                "prefix_reference": "http://schema.repronim.org/",
            },
            "schema": {
                "prefix_prefix": "schema",
                "prefix_reference": "http://schema.org/",
            },
            "skos": {
                "prefix_prefix": "skos",
                "prefix_reference": "http://www.w3.org/2004/02/skos/core#",
            },
            "xml": {
                "prefix_prefix": "xml",
                "prefix_reference": "http://www.w3.org/XML/1998/namespace",
            },
            "xsd": {
                "prefix_prefix": "xsd",
                "prefix_reference": "http://www.w3.org/2001/XMLSchema#",
            },
        },
        "source_file": "linkml-schema/reproschema.yaml",
    }
)


class AllowedType(str, Enum):
    AllowAltResponse = "reproschema:AllowAltResponse"
    """
    Indicates (by boolean) if alternate responses are allowed or not.
    """
    AllowExport = "reproschema:AllowExport"
    """
    Indicates (by boolean) if data can be exported or not.
    """
    AllowReplay = "reproschema:AllowReplay"
    """
    Indicates (by boolean) if items can be replayed or not.
    """
    AllowSkip = "reproschema:AllowSkip"
    """
    Indicates (by boolean) if items can be skipped or not.
    """
    AutoAdvance = "reproschema:AutoAdvance"
    """
    Indicates (by boolean) if assessments in a protocol can auto advance or not.
    """
    DisableBack = "reproschema:DisableBack"
    """
    Indicates (by boolean) if we can go back to a completed assessment in a protocol.
    """


class MissingType(str, Enum):
    Skipped = "reproschema:Skipped"
    """
    An element to describe the choice when the item is skipped.
    """
    DontKnow = "reproschema:DontKnow"
    """
    An element to describe the choice when response is not known.
    """
    Unknown = "reproschema:Unknown"
    """
    An element to describe the choice when the reason for missing response is unknown.
    """
    TimedOut = "reproschema:TimedOut"
    """
    A boolean element to describe if the response did not occur within the prescribed time.
    """


class Agent(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "prov:Agent",
            "from_schema": "http://schema.repronim.org/",
        }
    )
    pass


class Participant(Agent):
    """
    An Agent describing characteristics associated with a participant.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:Participant",
            "from_schema": "http://schema.repronim.org/",
            "title": "Participant",
        }
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    subject_id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "subject_id",
                "domain_of": ["Participant"],
                "slot_uri": "nidm:subject_id",
            }
        },
    )


class Thing(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "schema:Thing",
            "from_schema": "http://schema.repronim.org/",
        }
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class Activity(Thing):
    """
    An assessment in a protocol.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:Activity",
            "from_schema": "http://schema.repronim.org/",
            "title": "Activity",
        }
    )
    about: Optional[str] = Field(
        default=None,
        description="The subject matter of the Field.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "about",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:about",
            }
        },
    )
    altLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="alternate label",
        description="The alternate label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "altLabel",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "skos:altLabel",
            }
        },
    )
    associatedMedia: Optional[str] = Field(
        default=None,
        title="associatedMedia",
        description="A media object that encodes this creative work. This property is a synonym for encoding.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "associatedMedia",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:associatedMedia",
            }
        },
    )
    citation: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "citation",
                "domain_of": ["Activity"],
                "slot_uri": "schema:citation",
            }
        },
    )
    compute: Optional[list[ComputeSpecification]] = Field(
        default=None,
        title="computation",
        description="An array of objects indicating computations in an activity or protocol and maps it to the corresponding Item. scoring logic is a subset of all computations that could be performed and not all computations will be scoring. For example, one may want to do conversion from one unit to another.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "compute",
                "domain_of": ["Activity", "Protocol"],
                "slot_uri": "reproschema:compute",
            }
        },
    )
    cronTable: Optional[str] = Field(
        default=None,
        title="cronTable",
        json_schema_extra={
            "linkml_meta": {
                "alias": "cronTable",
                "domain_of": ["Activity", "Protocol"],
                "slot_uri": "reproschema:cronTable",
            }
        },
    )
    description: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:description",
            }
        },
    )
    image: Optional[Union[ImageObject, str]] = Field(
        default=None,
        title="image",
        description='An image of the item. This can be a <a class="localLink" href="http://schema.org/URL">URL</a> or a fully described <a class="localLink" href="http://schema.org/ImageObject">ImageObject</a>.',
        json_schema_extra={
            "linkml_meta": {
                "alias": "image",
                "any_of": [{"range": "ImageObject"}, {"range": "uri"}],
                "domain_of": ["Activity", "Choice", "Item"],
                "slot_uri": "schema:image",
            }
        },
    )
    isProprietary: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "isProprietary",
                "domain_of": ["Activity"],
                "slot_uri": "schema:isProprietary",
            }
        },
    )
    messages: Optional[list[MessageSpecification]] = Field(
        default=None,
        title="messages",
        description="An array of objects to define conditional messages in an activity or protocol.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "messages",
                "domain_of": ["Activity", "Protocol"],
                "slot_uri": "reproschema:messages",
            }
        },
    )
    preamble: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="Preamble",
        description="The preamble for an assessment.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "preamble",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "reproschema:preamble",
            }
        },
    )
    prefLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="preferred label",
        description="The preferred label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefLabel",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "OverrideProperty",
                    "Protocol",
                    "UnitOption",
                ],
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    schemaVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "schemaVersion",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:schemaVersion",
            }
        },
    )
    ui: Optional[UI] = Field(
        default=None,
        title="UI",
        description="An element to control UI specifications. Originally @nest in jsonld, but using a class in the model.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ui",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "Protocol",
                ],
                "slot_uri": "reproschema:ui",
            }
        },
    )
    version: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "version",
                "domain_of": ["Activity", "Item", "Protocol", "SoftwareAgent"],
                "slot_uri": "schema:version",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class AdditionalNoteObj(Thing):
    """
    A set of objects to define notes in a Item. For example, most Redcap and NDA data dictionaries have notes for each item which needs to be captured in reproschema
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:AdditionalNoteObj",
            "from_schema": "http://schema.repronim.org/",
            "title": "Additional Notes Object",
        }
    )
    column: Optional[str] = Field(
        default=None,
        title="column",
        description="An element to define the column name where the note was taken from.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "column",
                "domain_of": ["AdditionalNoteObj"],
                "slot_uri": "reproschema:column",
            }
        },
    )
    source: Optional[str] = Field(
        default=None,
        title="source",
        description="An element to define the source (eg. RedCap, NDA) where the note was taken from.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "source",
                "domain_of": ["AdditionalNoteObj"],
                "slot_uri": "reproschema:source",
            }
        },
    )
    value: Optional[
        Union[
            Dict[str, str], MissingType, StructuredValue, bool, float, int, str
        ]
    ] = Field(
        default=None,
        title="value",
        description="The value for each option in choices or in additionalNotesObj",
        json_schema_extra={
            "linkml_meta": {
                "alias": "value",
                "any_of": [
                    {"range": "float"},
                    {"range": "integer"},
                    {"range": "boolean"},
                    {"range": "StructuredValue"},
                    {"range": "langString"},
                    {"range": "uri"},
                    {"range": "string"},
                    {"range": "MissingType"},
                ],
                "domain_of": [
                    "AdditionalNoteObj",
                    "Choice",
                    "Response",
                    "UnitOption",
                ],
                "slot_uri": "schema:value",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class AdditionalProperty(Thing):
    """
    An object to describe the various properties added to assessments and Items.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:AdditionalProperty",
            "from_schema": "http://schema.repronim.org/",
            "title": "Additional properties",
        }
    )
    allow: Optional[list[AllowedType]] = Field(
        default=None,
        title="allow",
        description="An array of items indicating properties allowed on an activity or protocol.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "allow",
                "domain_of": ["AdditionalProperty", "UI"],
                "slot_uri": "reproschema:allow",
            }
        },
    )
    isAbout: Optional[Union[Activity, Item, str]] = Field(
        default=None,
        title="isAbout",
        description="A pointer to the node describing the item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "isAbout",
                "any_of": [
                    {"range": "uri"},
                    {"range": "Activity"},
                    {"range": "Item"},
                ],
                "domain_of": [
                    "AdditionalProperty",
                    "OverrideProperty",
                    "Response",
                ],
                "slot_uri": "reproschema:isAbout",
            }
        },
    )
    isVis: Optional[Union[bool, str]] = Field(
        default=None,
        title="visibility",
        description="An element to describe (by boolean or conditional statement) visibility conditions of items in an assessment.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "isVis",
                "any_of": [{"range": "boolean"}, {"range": "string"}],
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:isVis",
            }
        },
    )
    limit: Optional[str] = Field(
        default=None,
        title="limit",
        description="An element to limit the duration (uses ISO 8601) this activity is allowed to be completed by once activity is available.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "limit",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:limit",
            }
        },
    )
    maxRetakes: Optional[int] = Field(
        default=None,
        title="maxRetakes",
        description="Defines number of times the item is allowed to be redone.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "maxRetakes",
                "any_of": [{"range": "integer"}],
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:maxRetakes",
            }
        },
    )
    prefLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="preferred label",
        description="The preferred label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefLabel",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "OverrideProperty",
                    "Protocol",
                    "UnitOption",
                ],
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    randomMaxDelay: Optional[str] = Field(
        default=None,
        title="randomMaxDelay",
        description="Present activity/item within some random offset of activity available time up to the maximum specified by this ISO 8601 duration",
        json_schema_extra={
            "linkml_meta": {
                "alias": "randomMaxDelay",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:randomMaxDelay",
            }
        },
    )
    schedule: Optional[str] = Field(
        default=None,
        title="Schedule",
        description="An element to set make activity available/repeat info using ISO 8601 repeating interval format.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "schedule",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:schedule",
            }
        },
    )
    valueRequired: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "valueRequired",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "schema:valueRequired",
            }
        },
    )
    variableName: Optional[str] = Field(
        default=None,
        title="variableName",
        description="The name used to represent an item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "variableName",
                "domain_of": [
                    "AdditionalProperty",
                    "ComputeSpecification",
                    "OverrideProperty",
                ],
                "slot_uri": "reproschema:variableName",
            }
        },
    )
    ui: Optional[UI] = Field(
        default=None,
        title="UI",
        description="An element to control UI specifications. Originally @nest in jsonld, but using a class in the model.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ui",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "Protocol",
                ],
                "slot_uri": "reproschema:ui",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class Choice(Thing):
    """
    An object to describe a response option.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:Choice",
            "from_schema": "http://schema.repronim.org/",
            "title": "Response choice",
        }
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    image: Optional[Union[ImageObject, str]] = Field(
        default=None,
        title="image",
        description='An image of the item. This can be a <a class="localLink" href="http://schema.org/URL">URL</a> or a fully described <a class="localLink" href="http://schema.org/ImageObject">ImageObject</a>.',
        json_schema_extra={
            "linkml_meta": {
                "alias": "image",
                "any_of": [{"range": "ImageObject"}, {"range": "uri"}],
                "domain_of": ["Activity", "Choice", "Item"],
                "slot_uri": "schema:image",
            }
        },
    )
    value: Optional[
        Union[
            Dict[str, str], MissingType, StructuredValue, bool, float, int, str
        ]
    ] = Field(
        default=None,
        title="value",
        description="The value for each option in choices or in additionalNotesObj",
        json_schema_extra={
            "linkml_meta": {
                "alias": "value",
                "any_of": [
                    {"range": "float"},
                    {"range": "integer"},
                    {"range": "boolean"},
                    {"range": "StructuredValue"},
                    {"range": "langString"},
                    {"range": "uri"},
                    {"range": "string"},
                    {"range": "MissingType"},
                ],
                "domain_of": [
                    "AdditionalNoteObj",
                    "Choice",
                    "Response",
                    "UnitOption",
                ],
                "slot_uri": "schema:value",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class ComputeSpecification(Thing):
    """
    An object to define computations in an activity or protocol.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:ComputeSpecification",
            "from_schema": "http://schema.repronim.org/",
            "title": "Compute Specification",
        }
    )
    jsExpression: Optional[str] = Field(
        default=None,
        title="JavaScript Expression",
        description="A JavaScript expression for computations. A JavaScript expression to compute a score from other variables.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "jsExpression",
                "domain_of": ["ComputeSpecification", "MessageSpecification"],
                "slot_uri": "reproschema:jsExpression",
            }
        },
    )
    variableName: Optional[str] = Field(
        default=None,
        title="variableName",
        description="The name used to represent an item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "variableName",
                "domain_of": [
                    "AdditionalProperty",
                    "ComputeSpecification",
                    "OverrideProperty",
                ],
                "slot_uri": "reproschema:variableName",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class Item(Thing):
    """
    An item in an assessment.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:Field",
            "from_schema": "http://schema.repronim.org/",
            "title": "Item in an activity",
        }
    )
    about: Optional[str] = Field(
        default=None,
        description="The subject matter of the Field.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "about",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:about",
            }
        },
    )
    additionalNotesObj: Optional[list[AdditionalNoteObj]] = Field(
        default=None,
        title="additional notes",
        description="A set of objects to define notes in a field. For example, most Redcap and NDA data dictionaries have notes for each item which needs to be captured in reproschema.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "additionalNotesObj",
                "any_of": [{"range": "AdditionalNoteObj"}],
                "domain_of": ["Item"],
                "slot_uri": "reproschema:additionalNotesObj",
            }
        },
    )
    altLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="alternate label",
        description="The alternate label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "altLabel",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "skos:altLabel",
            }
        },
    )
    associatedMedia: Optional[str] = Field(
        default=None,
        title="associatedMedia",
        description="A media object that encodes this creative work. This property is a synonym for encoding.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "associatedMedia",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:associatedMedia",
            }
        },
    )
    audio: Optional[Union[AudioObject, str]] = Field(
        default=None,
        title="audio",
        description="An audio object.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "audio",
                "any_of": [{"range": "uri"}, {"range": "AudioObject"}],
                "domain_of": ["Item"],
                "slot_uri": "schema:audio",
            }
        },
    )
    backgroundImage: Optional[Union[ImageObject, str]] = Field(
        default=None,
        title="backgroundImage",
        description="Background image for drawing activities.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "backgroundImage",
                "any_of": [{"range": "ImageObject"}, {"range": "uri"}],
                "domain_of": ["Item"],
                "slot_uri": "reproschema:backgroundImage",
            }
        },
    )
    description: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:description",
            }
        },
    )
    image: Optional[Union[ImageObject, str]] = Field(
        default=None,
        title="image",
        description='An image of the item. This can be a <a class="localLink" href="http://schema.org/URL">URL</a> or a fully described <a class="localLink" href="http://schema.org/ImageObject">ImageObject</a>.',
        json_schema_extra={
            "linkml_meta": {
                "alias": "image",
                "any_of": [{"range": "ImageObject"}, {"range": "uri"}],
                "domain_of": ["Activity", "Choice", "Item"],
                "slot_uri": "schema:image",
            }
        },
    )
    isPartOf: Optional[Activity] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "isPartOf",
                "domain_of": ["Item"],
                "slot_uri": "schema:isPartOf",
            }
        },
    )
    preamble: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="Preamble",
        description="The preamble for an assessment.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "preamble",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "reproschema:preamble",
            }
        },
    )
    prefLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="preferred label",
        description="The preferred label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefLabel",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "OverrideProperty",
                    "Protocol",
                    "UnitOption",
                ],
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    question: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "question",
                "domain_of": ["Item"],
                "slot_uri": "schema:question",
            }
        },
    )
    responseOptions: Optional[Union[ResponseOption, str]] = Field(
        default=None,
        title="Response options",
        description="An element (object or by URL)to describe the properties of response of the Item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "responseOptions",
                "any_of": [{"range": "uri"}, {"range": "ResponseOption"}],
                "domain_of": ["Item"],
                "slot_uri": "reproschema:responseOptions",
            }
        },
    )
    schemaVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "schemaVersion",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:schemaVersion",
            }
        },
    )
    ui: Optional[UI] = Field(
        default=None,
        title="UI",
        description="An element to control UI specifications. Originally @nest in jsonld, but using a class in the model.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ui",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "Protocol",
                ],
                "slot_uri": "reproschema:ui",
            }
        },
    )
    version: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "version",
                "domain_of": ["Activity", "Item", "Protocol", "SoftwareAgent"],
                "slot_uri": "schema:version",
            }
        },
    )
    video: Optional[Union[VideoObject, str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "video",
                "any_of": [{"range": "VideoObject"}, {"range": "uri"}],
                "domain_of": ["Item"],
                "slot_uri": "schema:video",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class LandingPage(Thing):
    """
    An object to define the landing page of a protocol.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:LandingPage",
            "from_schema": "http://schema.repronim.org/",
            "title": "Landing Page",
        }
    )
    inLanguage: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "inLanguage",
                "domain_of": [
                    "LandingPage",
                    "MediaObject",
                    "ResponseActivity",
                ],
                "slot_uri": "schema:inLanguage",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class MediaObject(Thing):
    """
    A media object, such as an image, video, audio, or text object embedded in a web page or a downloadable dataset.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "schema:MediaObject",
            "from_schema": "http://schema.repronim.org/",
            "slot_usage": {
                "contentUrl": {"name": "contentUrl", "required": True}
            },
            "title": "Media Object",
        }
    )
    inLanguage: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "inLanguage",
                "domain_of": [
                    "LandingPage",
                    "MediaObject",
                    "ResponseActivity",
                ],
                "slot_uri": "schema:inLanguage",
            }
        },
    )
    contentUrl: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "contentUrl",
                "domain_of": ["MediaObject"],
                "slot_uri": "schema:contentUrl",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class AudioObject(MediaObject):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "schema:AudioObject",
            "from_schema": "http://schema.repronim.org/",
        }
    )
    inLanguage: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "inLanguage",
                "domain_of": [
                    "LandingPage",
                    "MediaObject",
                    "ResponseActivity",
                ],
                "slot_uri": "schema:inLanguage",
            }
        },
    )
    contentUrl: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "contentUrl",
                "domain_of": ["MediaObject"],
                "slot_uri": "schema:contentUrl",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class ImageObject(MediaObject):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "schema:ImageObject",
            "from_schema": "http://schema.repronim.org/",
        }
    )
    inLanguage: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "inLanguage",
                "domain_of": [
                    "LandingPage",
                    "MediaObject",
                    "ResponseActivity",
                ],
                "slot_uri": "schema:inLanguage",
            }
        },
    )
    contentUrl: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "contentUrl",
                "domain_of": ["MediaObject"],
                "slot_uri": "schema:contentUrl",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class MessageSpecification(Thing):
    """
    An object to define messages in an activity or protocol.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:MessageSpecification",
            "from_schema": "http://schema.repronim.org/",
            "title": "Message Specification",
        }
    )
    jsExpression: Optional[str] = Field(
        default=None,
        title="JavaScript Expression",
        description="A JavaScript expression for computations. A JavaScript expression to compute a score from other variables.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "jsExpression",
                "domain_of": ["ComputeSpecification", "MessageSpecification"],
                "slot_uri": "reproschema:jsExpression",
            }
        },
    )
    message: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="Message",
        description="The message to be conditionally displayed for an item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "message",
                "domain_of": ["MessageSpecification"],
                "slot_uri": "reproschema:message",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class OverrideProperty(Thing):
    """
    An object to override the various properties added to assessments and Items.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:OverrideProperty",
            "from_schema": "http://schema.repronim.org/",
            "title": "Additional properties",
        }
    )
    isAbout: Optional[Union[Activity, Item, str]] = Field(
        default=None,
        title="isAbout",
        description="A pointer to the node describing the item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "isAbout",
                "any_of": [
                    {"range": "uri"},
                    {"range": "Activity"},
                    {"range": "Item"},
                ],
                "domain_of": [
                    "AdditionalProperty",
                    "OverrideProperty",
                    "Response",
                ],
                "slot_uri": "reproschema:isAbout",
            }
        },
    )
    isVis: Optional[Union[bool, str]] = Field(
        default=None,
        title="visibility",
        description="An element to describe (by boolean or conditional statement) visibility conditions of items in an assessment.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "isVis",
                "any_of": [{"range": "boolean"}, {"range": "string"}],
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:isVis",
            }
        },
    )
    limit: Optional[str] = Field(
        default=None,
        title="limit",
        description="An element to limit the duration (uses ISO 8601) this activity is allowed to be completed by once activity is available.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "limit",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:limit",
            }
        },
    )
    maxRetakes: Optional[int] = Field(
        default=None,
        title="maxRetakes",
        description="Defines number of times the item is allowed to be redone.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "maxRetakes",
                "any_of": [{"range": "integer"}],
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:maxRetakes",
            }
        },
    )
    prefLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="preferred label",
        description="The preferred label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefLabel",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "OverrideProperty",
                    "Protocol",
                    "UnitOption",
                ],
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    randomMaxDelay: Optional[str] = Field(
        default=None,
        title="randomMaxDelay",
        description="Present activity/item within some random offset of activity available time up to the maximum specified by this ISO 8601 duration",
        json_schema_extra={
            "linkml_meta": {
                "alias": "randomMaxDelay",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:randomMaxDelay",
            }
        },
    )
    schedule: Optional[str] = Field(
        default=None,
        title="Schedule",
        description="An element to set make activity available/repeat info using ISO 8601 repeating interval format.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "schedule",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "reproschema:schedule",
            }
        },
    )
    valueRequired: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "valueRequired",
                "domain_of": ["AdditionalProperty", "OverrideProperty"],
                "slot_uri": "schema:valueRequired",
            }
        },
    )
    variableName: Optional[str] = Field(
        default=None,
        title="variableName",
        description="The name used to represent an item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "variableName",
                "domain_of": [
                    "AdditionalProperty",
                    "ComputeSpecification",
                    "OverrideProperty",
                ],
                "slot_uri": "reproschema:variableName",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class Protocol(Thing):
    """
    A representation of a study which comprises one or more assessments.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:Protocol",
            "from_schema": "http://schema.repronim.org/",
            "title": "Protocol",
        }
    )
    about: Optional[str] = Field(
        default=None,
        description="The subject matter of the Field.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "about",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:about",
            }
        },
    )
    altLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="alternate label",
        description="The alternate label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "altLabel",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "skos:altLabel",
            }
        },
    )
    associatedMedia: Optional[str] = Field(
        default=None,
        title="associatedMedia",
        description="A media object that encodes this creative work. This property is a synonym for encoding.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "associatedMedia",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:associatedMedia",
            }
        },
    )
    compute: Optional[list[ComputeSpecification]] = Field(
        default=None,
        title="computation",
        description="An array of objects indicating computations in an activity or protocol and maps it to the corresponding Item. scoring logic is a subset of all computations that could be performed and not all computations will be scoring. For example, one may want to do conversion from one unit to another.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "compute",
                "domain_of": ["Activity", "Protocol"],
                "slot_uri": "reproschema:compute",
            }
        },
    )
    cronTable: Optional[str] = Field(
        default=None,
        title="cronTable",
        json_schema_extra={
            "linkml_meta": {
                "alias": "cronTable",
                "domain_of": ["Activity", "Protocol"],
                "slot_uri": "reproschema:cronTable",
            }
        },
    )
    description: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:description",
            }
        },
    )
    landingPage: Optional[list[Union[LandingPage, str]]] = Field(
        default=None,
        title="Landing page content",
        description="An element (by URL) to point to the protocol readme or landing page.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "landingPage",
                "any_of": [
                    {"range": "uri"},
                    {"range": "string"},
                    {"range": "LandingPage"},
                ],
                "domain_of": ["Protocol"],
                "slot_uri": "reproschema:landingPage",
            }
        },
    )
    messages: Optional[list[MessageSpecification]] = Field(
        default=None,
        title="messages",
        description="An array of objects to define conditional messages in an activity or protocol.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "messages",
                "domain_of": ["Activity", "Protocol"],
                "slot_uri": "reproschema:messages",
            }
        },
    )
    preamble: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="Preamble",
        description="The preamble for an assessment.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "preamble",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "reproschema:preamble",
            }
        },
    )
    prefLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="preferred label",
        description="The preferred label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefLabel",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "OverrideProperty",
                    "Protocol",
                    "UnitOption",
                ],
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    schemaVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "schemaVersion",
                "domain_of": ["Activity", "Item", "Protocol"],
                "slot_uri": "schema:schemaVersion",
            }
        },
    )
    ui: Optional[UI] = Field(
        default=None,
        title="UI",
        description="An element to control UI specifications. Originally @nest in jsonld, but using a class in the model.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "ui",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "Protocol",
                ],
                "slot_uri": "reproschema:ui",
            }
        },
    )
    version: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "version",
                "domain_of": ["Activity", "Item", "Protocol", "SoftwareAgent"],
                "slot_uri": "schema:version",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class Response(Thing):
    """
    Describes the response of an item.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:Response",
            "from_schema": "http://schema.repronim.org/",
            "title": "Response",
        }
    )
    isAbout: Optional[Union[Activity, Item, str]] = Field(
        default=None,
        title="isAbout",
        description="A pointer to the node describing the item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "isAbout",
                "any_of": [
                    {"range": "uri"},
                    {"range": "Activity"},
                    {"range": "Item"},
                ],
                "domain_of": [
                    "AdditionalProperty",
                    "OverrideProperty",
                    "Response",
                ],
                "slot_uri": "reproschema:isAbout",
            }
        },
    )
    value: Optional[
        Union[
            Dict[str, str], MissingType, StructuredValue, bool, float, int, str
        ]
    ] = Field(
        default=None,
        title="value",
        description="The value for each option in choices or in additionalNotesObj",
        json_schema_extra={
            "linkml_meta": {
                "alias": "value",
                "any_of": [
                    {"range": "float"},
                    {"range": "integer"},
                    {"range": "boolean"},
                    {"range": "StructuredValue"},
                    {"range": "langString"},
                    {"range": "uri"},
                    {"range": "string"},
                    {"range": "MissingType"},
                ],
                "domain_of": [
                    "AdditionalNoteObj",
                    "Choice",
                    "Response",
                    "UnitOption",
                ],
                "slot_uri": "schema:value",
            }
        },
    )
    wasAttributedTo: Optional[Participant] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "wasAttributedTo",
                "domain_of": ["Response"],
                "slot_uri": "prov:wasAttributedTo",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class ResponseActivity(Thing):
    """
    Captures information about some action that took place. It also links to information (entities) that were used during the activity
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:ResponseActivity",
            "from_schema": "http://schema.repronim.org/",
            "title": "ResponseActivity",
        }
    )
    endedAtTime: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "endedAtTime",
                "domain_of": ["ResponseActivity"],
                "slot_uri": "prov:endedAtTime",
            }
        },
    )
    generated: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "generated",
                "domain_of": ["ResponseActivity"],
                "slot_uri": "prov:generated",
            }
        },
    )
    inLanguage: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "inLanguage",
                "domain_of": [
                    "LandingPage",
                    "MediaObject",
                    "ResponseActivity",
                ],
                "slot_uri": "schema:inLanguage",
            }
        },
    )
    startedAtTime: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "startedAtTime",
                "domain_of": ["ResponseActivity"],
                "slot_uri": "prov:startedAtTime",
            }
        },
    )
    used: Optional[list[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "used",
                "domain_of": ["ResponseActivity"],
                "slot_uri": "prov:used",
            }
        },
    )
    wasAssociatedWith: Optional[SoftwareAgent] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "wasAssociatedWith",
                "domain_of": ["ResponseActivity"],
                "slot_uri": "prov:wasAssociatedWith",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class ResponseOption(Thing):
    """
    An element (object or by URL)to describe the properties of response of the Item.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:ResponseOption",
            "from_schema": "http://schema.repronim.org/",
            "title": "Response option",
        }
    )
    choices: Optional[list[Union[Choice, str]]] = Field(
        default=None,
        title="choices",
        description="An array to list the available options for response of the Item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "choices",
                "any_of": [{"range": "uri"}, {"range": "Choice"}],
                "domain_of": ["ResponseOption"],
                "exact_mappings": ["schema:itemListElement"],
                "slot_uri": "reproschema:choices",
            }
        },
    )
    datumType: Optional[str] = Field(
        default=None,
        title="datumType",
        description="Indicates what type of datum the response is (e.g. range,count,scalar etc.) for the Item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "datumType",
                "any_of": [{"range": "string"}, {"range": "uri"}],
                "domain_of": ["ResponseOption"],
                "slot_uri": "reproschema:datumType",
            }
        },
    )
    maxValue: Optional[Union[float, int]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "maxValue",
                "any_of": [{"range": "float"}, {"range": "integer"}],
                "domain_of": ["ResponseOption"],
                "slot_uri": "schema:maxValue",
            }
        },
    )
    minValue: Optional[Union[float, int]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "minValue",
                "any_of": [{"range": "float"}, {"range": "integer"}],
                "domain_of": ["ResponseOption"],
                "slot_uri": "schema:minValue",
            }
        },
    )
    multipleChoice: Optional[bool] = Field(
        default=None,
        title="Multiple choice response expectation",
        description="Indicates (by bool) if response for the Item has one or more answer.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "multipleChoice",
                "domain_of": ["ResponseOption"],
                "slot_uri": "reproschema:multipleChoice",
            }
        },
    )
    unitOptions: Optional[list[UnitOption]] = Field(
        default=None,
        title="unitOptions",
        description="A list of objects to represent a human displayable name alongside the more formal value for units.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "unitOptions",
                "domain_of": ["ResponseOption"],
                "slot_uri": "reproschema:unitOptions",
            }
        },
    )
    valueType: Optional[list[str]] = Field(
        default=None,
        title="The type of the response",
        description="The type of the response of an item. For example, string, integer, etc.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "valueType",
                "domain_of": ["ResponseOption"],
                "slot_uri": "reproschema:valueType",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class SoftwareAgent(Thing):
    """
    Captures information about some action that took place. It also links to information (entities) that were used during the activity
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:SoftwareAgent",
            "from_schema": "http://schema.repronim.org/",
            "title": "Software Agent",
        }
    )
    version: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "version",
                "domain_of": ["Activity", "Item", "Protocol", "SoftwareAgent"],
                "slot_uri": "schema:version",
            }
        },
    )
    url: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "url",
                "domain_of": ["SoftwareAgent"],
                "slot_uri": "schema:url",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class StructuredValue(Thing):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "schema:StructuredValue",
            "from_schema": "http://schema.repronim.org/",
        }
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class UI(ConfiguredBaseModel):
    """
    A group of properties related to UI.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:UI",
            "from_schema": "http://schema.repronim.org/",
            "title": "UI properties",
        }
    )
    order: Optional[list[Union[Activity, Item, str]]] = Field(
        default=None,
        title="Order",
        description="An ordered list to describe the order in which the items of an assessment or protocol appear in the user interface.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "order",
                "any_of": [
                    {"range": "uri"},
                    {"range": "Activity"},
                    {"range": "Item"},
                ],
                "domain_of": ["UI"],
                "slot_uri": "reproschema:order",
            }
        },
    )
    addProperties: Optional[list[AdditionalProperty]] = Field(
        default=None,
        title="addProperties",
        description="An array of objects to describe the various properties added to assessments and Items.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "addProperties",
                "domain_of": ["UI"],
                "slot_uri": "reproschema:addProperties",
            }
        },
    )
    overrideProperties: Optional[list[OverrideProperty]] = Field(
        default=None,
        title="overrideProperties",
        description="An array of objects to override the various properties added to assessments and fields.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "overrideProperties",
                "domain_of": ["UI"],
                "slot_uri": "reproschema:overrideProperties",
            }
        },
    )
    shuffle: Optional[bool] = Field(
        default=None,
        title="Shuffle",
        description="An element (bool) to determine if the list of items is shuffled or in order.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "shuffle",
                "domain_of": ["UI"],
                "slot_uri": "reproschema:shuffle",
            }
        },
    )
    allow: Optional[list[AllowedType]] = Field(
        default=None,
        title="allow",
        description="An array of items indicating properties allowed on an activity or protocol.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "allow",
                "domain_of": ["AdditionalProperty", "UI"],
                "slot_uri": "reproschema:allow",
            }
        },
    )
    inputType: Optional[str] = Field(
        default=None,
        title="inputType",
        description="An element to describe the input type of a Item.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "inputType",
                "domain_of": ["UI"],
                "slot_uri": "reproschema:inputType",
            }
        },
    )
    readonlyValue: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "readonlyValue",
                "domain_of": ["UI"],
                "slot_uri": "schema:readonlyValue",
            }
        },
    )


class UnitOption(Thing):
    """
    An object to represent a human displayable name alongside the more formal value for units.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "reproschema:UnitOption",
            "from_schema": "http://schema.repronim.org/",
            "slot_usage": {
                "value": {
                    "any_of": [{"range": "uri"}, {"range": "langString"}],
                    "name": "value",
                }
            },
            "title": "Unit options",
        }
    )
    prefLabel: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        title="preferred label",
        description="The preferred label.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefLabel",
                "domain_of": [
                    "Activity",
                    "AdditionalProperty",
                    "Item",
                    "OverrideProperty",
                    "Protocol",
                    "UnitOption",
                ],
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    value: Optional[Union[Dict[str, str], str]] = Field(
        default=None,
        title="value",
        description="The value for each option in choices or in additionalNotesObj",
        json_schema_extra={
            "linkml_meta": {
                "alias": "value",
                "any_of": [{"range": "uri"}, {"range": "langString"}],
                "domain_of": [
                    "AdditionalNoteObj",
                    "Choice",
                    "Response",
                    "UnitOption",
                ],
                "slot_uri": "schema:value",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


class VideoObject(MediaObject):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "schema:VideoObject",
            "from_schema": "http://schema.repronim.org/",
            "title": "Video Object",
        }
    )
    inLanguage: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "inLanguage",
                "domain_of": [
                    "LandingPage",
                    "MediaObject",
                    "ResponseActivity",
                ],
                "slot_uri": "schema:inLanguage",
            }
        },
    )
    contentUrl: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "contentUrl",
                "domain_of": ["MediaObject"],
                "slot_uri": "schema:contentUrl",
            }
        },
    )
    id: Optional[str] = Field(
        default=None,
        description="A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": ["Participant", "Thing"],
                "slot_uri": "schema:identifier",
            }
        },
    )
    name: Optional[dict[str, Union[str, Dict[str, str]]]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Choice", "Thing"],
                "slot_uri": "schema:name",
            }
        },
    )
    category: Optional[str] = Field(
        default=None,
        description="Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In an RDF database it should be a model class URI. This field is multi-valued.",
        json_schema_extra={
            "linkml_meta": {
                "alias": "category",
                "domain_of": ["Thing"],
                "slot_uri": "rdf:type",
            }
        },
    )


Agent.model_rebuild()
Participant.model_rebuild()
Thing.model_rebuild()
Activity.model_rebuild()
AdditionalNoteObj.model_rebuild()
AdditionalProperty.model_rebuild()
Choice.model_rebuild()
ComputeSpecification.model_rebuild()
Item.model_rebuild()
LandingPage.model_rebuild()
MediaObject.model_rebuild()
AudioObject.model_rebuild()
ImageObject.model_rebuild()
MessageSpecification.model_rebuild()
OverrideProperty.model_rebuild()
Protocol.model_rebuild()
Response.model_rebuild()
ResponseActivity.model_rebuild()
ResponseOption.model_rebuild()
SoftwareAgent.model_rebuild()
StructuredValue.model_rebuild()
UI.model_rebuild()
UnitOption.model_rebuild()
VideoObject.model_rebuild()
