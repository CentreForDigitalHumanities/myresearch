# Using GraphQLList

For list pages in MyResearch, we use GraphQLList. This is a custom implementation of UUList, which is itself a custom Vue component for rendering lists, part of [CDH Vue-lib](https://github.com/CentreForDigitalHumanities/Vue-lib). GraphQLList has originally been developed for use in the [DIAPP](https://github.com/CentreForDigitalHumanities/DIAPP). For now (Nov. 2025), we have simply copied this implementation into MyResearch, but ideally, these Vue components and custom Graphene/Django objects used for GraphQLList, should live in a separate library for other portals using the Vue/GraphQL/Django stack. This is a quick piece of documentation to explain how to use GraphQLList, as there are a lot of moving parts.

## What does GraphQLList do?

GraphQLList produces a nicely styled list, based on a GraphQL query to the backend. It can be made searchable and have custom ordering and filters.

## Preparing a Query

Let's try to make a GQLList for a hypothetical `Book` object.

To prepare a query, we first need to ensure that we are using our custom override of Graphene's DjangoObjectType: GQLListObjectType. This allows us to add fields to DjangoObjectType's Meta. In the ObjectType, we can also specify which fields should be searchable and what kind of filters we would like to have available for this object. We could for instance make the `Book`'s ObjectType look something like this:

```
class BookFilter(FilterSet):

    color_ids = ModelMultipleChoiceFilter(
        field_name="color_id", queryset=Color.objects.all()
    )


class BookType(GQLListObjectType):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "color",
        ]
        filterset_class = BookFilter
        search_fields = [
            "title",
            "author",
        ]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[Book],
        info: ResolveInfo,
    ) -> QuerySet[Book]:
        return queryset

```
This ensures that the `Book`'s Title and Author are searchable and the we can filter the list of books based on its color (supposing this is a related object in this case). For more information on how to write filters, check out the docs for [django-filter](https://django-filter.readthedocs.io/en/stable/index.html).

Next, we need to add a `book_pages` query to our `BookQuery` object. This uses a custom field object, which adds some relevant attributes to a list-like query for pagination. The field is called `GQLListPaginationConnectionField`. Add the field to your query object like so:

```
    book_pages = GQLListPaginationConnectionField(
        BookType,
    )
```
With a resolver, that will look similar to other List resolvers:
```
    @staticmethod
    def resolve_book_pages(root, info: ResolveInfo, **kwargs) -> QuerySet[Book]:
        return BookType.get_queryset(Book.objects, info)
```
This is all the work in the backend done!
## Rendering your query using GraphQLList
Next we'll render the result of this query using our GraphQLList component. First, create a new page where you want your list to live. Then we'll need to setup a few things. The most important thing is your GraphQL query, which might look something like this:
```
const GET_STUDY_PAGES = graphql(`
query GetStudyPages(
  $limit: Int
  $offset: Int
  $ordering: String
  $search: String
  $colorIds: [ID]
) {
  studyPages(
    mrPermission: "View"
    limit: $limit
    offset: $offset
    ordering: $ordering
    search: $search
    colorIds: $colorIds
  ) {
    results {
      id
      title
      author
      color {
        id
        value
        name
      }
    }
    pageInfo {
      count
      limit
      offset
    }
  }
}
```
There is some extra variables here, which are provided via GQLListPaginationConnectionField. Furthermore, there is also the variable that we use for our filter (`colorIds`). Our `Book` objects are available in the `result` property of the query result.

Next, we'll need to define the variable that we are passing into our GraphQLList component. These are kindoff like default variables for search and ordering. In our case they might look like this:
```
const variables = ref<GraphQLListVariables>({
    search: "",
    ordering: "title",
    colorIds: [], 
});
```
We can also specify the ordering options that we'd like to be available. This can be done like so:
```
const orderingOptions = computed(() => {
    return [
        {
            field: "title",
            label: t("title ascending"),
        },
        {
            field: "-title",
            label: t("title descending"),
        },
        {
            field: "color__name",
            label: t("color ascending"),
        },
        {
            field: "-color__name",
            label: t("color descending"),
        },
    ];
});
```
Using a `-` to precede a field orders it in a descending order. Note, that to access a field of a related model (`color.name` in our case) we can use double underscores.

Next, we'll need to specify the frontend look for our filter. It can be useful to perform a secondary query if we're using related models for a filter. We'll use this secondary query to populate the choices for our filter. This can be done like this:
```
const GET_COLORS = graphql(`
query getColors {
  colors {
    id
    name
  }
}
`)

const { result } = useQuery<GetColorsQuery>(GET_COLORS);

const colors = computed(() => result.value?.colors ?? []);

const filters = computed<UUListTypes.FilterDefinition[]>(() => {
    const colorFilter: UUListTypes.FilterDefinition = {
        field: "colorIds",
        label: t("Color"),
        // Would be better to have a type for color instead of any!
        options: colors.value.map((color: any) => [
            // the value for the filter
            color.id,
            // the label for the filter
            color.name,
        ]),
        type: "checkbox",
        initial: [],
    };
    return [colorFilter];
});

```
Now we are ready to move onto the template part of our vue file. The component's body is structured like a HTML table. So what we place inside our template tag could look like this:
```
    <GraphQLList
        v-model:variables="variables"
        :query-document="GET_BOOK_PAGES"
        <!--Would be better to have a type for color instead of any!-->
        :data-mapper="(result: any) => result?.bookPages ?? undefined"
        :ordering-options="orderingOptions"
        :filters="filters"
        fetch-policy="no-cache"
    >
        <template #data="{ data, isLoading }">
            <table class="table table-hover table-striped">
                <!--Define the headers for your list-->
                <thead>
                    <tr>
                        <th>
                            {{ $t("Title") }}
                        </th>
                        <th>
                            {{ $t("Author") }}
                        </th>
                        <th>
                            {{ $t("Color") }}
                        </th>
                    </tr>
                </thead>
                <!--Define the contents of the cells-->
                <tbody>
                    <tr v-for="row in data" :key="row.id">
                        <td class="align-middle">
                            {{ row.title }}
                        </td>
                        <td>
                            {{ row.author }}
                        </td>
                        <td>
                            {{ row.color.name }}
                        </td>
                    </tr>
                    <tr v-if="isLoading">
                        <td colspan="5" class="text-center">
                            <Loading />
                        </td>
                    </tr>
                    <tr v-if="!isLoading && data?.length === 0">
                        <td colspan="5" class="text-center">
                            {{ $t("errors.no_results_found") }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </template>
    </GraphQLList>
```
Now you should have a basic GraphQLList up and running!

There are more advanced options for filtering and using GraphQLList. Have a look at the [DIAPP](https://github.com/CentreForDigitalHumanities/DIAPP) for more inspiration. I hope this was helpful.

Last edited: 20-11-2025