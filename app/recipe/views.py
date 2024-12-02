from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manage recipes in the database.

    This viewset provides CRUD operations for Recipe objects:
    * List all recipes
    * Create a new recipe
    * Retrieve a specific recipe
    * Update a recipe
    * Delete a recipe

    Authentication is required for all operations.
    Users can only access their own recipes.
    """

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve recipes for the authenticated user.
        Returns recipes sorted by ID in descending order.
        """
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """
        Return appropriate serializer class.

        Returns:
            RecipeDetailSerializer for retrieve actions
            RecipeSerializer for all other actions
        """
        if self.action == "retrieve" or self.action == "update":
            return serializers.RecipeDetailSerializer
        elif self.action == "upload_image":  # our custom action
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe with the authenticated user."""
        serializer.save(user=self.request.user)

    # detail = True is the endpoint for model-detail
    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):  # custom action
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
